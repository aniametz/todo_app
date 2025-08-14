from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from functions import convert_iso_to_datetime, create_tag_objects
from Levenshtein import distance, hamming

from data_models.todo import Todo
from data_models.tag import Tag
from data_models.todo_tag_association import TodoTagAssociation
from database import db

from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()

@app.route('/create_todo', methods=["POST"])
def create_todo():
    data = request.get_json().get("todoData")
    data["dueDate"] = convert_iso_to_datetime(data["dueDate"])
    tag_objects = create_tag_objects(data)
    new_todo = Todo(**data)
    new_todo.tags = tag_objects
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'success'})

@app.route('/update_todo', methods=["POST"])
def update_todo():
    data = request.get_json().get("todoData")
    data["dueDate"] = convert_iso_to_datetime(data["dueDate"])
    data["completedAt"] = datetime.now(timezone.utc) if data["isDone"] else None
    # createdAt should not be updated (besides its fromat from svelte is not compatible with the database)
    data.pop("createdAt", None)  
    tag_objects = create_tag_objects(data)
    Todo.query.filter_by(id=data["id"]).update(data)
    # tags should not be updated in bulk
    todo = Todo.query.filter_by(id=data["id"]).first()
    todo.tags[:] = tag_objects
    db.session.commit()
    return jsonify({'message': 'success'})

@app.route('/delete_todo', methods=["POST"])
def delete_todo():
    data = request.get_json().get("todoData")
    Todo.query.filter_by(id=data).delete()
    db.session.commit()
    return jsonify({'message': 'success'})

@app.route('/get_todos')
def get_todos():
    todos = Todo.query.all()
    return jsonify({"todos": [t.as_dict() for t in todos]})

@app.route('/validate_tag', methods=["POST"])
def validate_tag():
    data = request.get_json().get("tagData")
    tags = Tag.query.all()
    for tag in tags:
        lower_tag_name = tag.name.strip().lower()
        lower_data_name = data["name"].strip().lower()
        if lower_tag_name == lower_data_name:
            return jsonify({'message': f'Tag "{tag.name}" already exists'})
        if hamming(lower_tag_name, lower_data_name) <= 2:
            return jsonify({'message': f'Tag name "{data["name"]}" is too similar to an existing tag "{tag.name}"'})
        if distance(lower_tag_name, lower_data_name) <= 4:
            return jsonify({'message': f'Tag name "{data["name"]}" is too similar to an existing tag "{tag.name}"'})
    return jsonify({'message': 'success'})

@app.route('/create_tag', methods=["POST"])
def create_tag():
    data = request.get_json().get("tagData")
    data["name"] = data["name"].strip()
    new_tag = Tag(**data)
    db.session.add(new_tag)
    db.session.commit()
    return jsonify({'message': 'success'})

@app.route('/delete_tag', methods=["POST"])
def delete_tag():
    data = request.get_json().get("tagData")
    Tag.query.filter_by(id=data).delete()
    TodoTagAssociation.query.filter_by(tag_id=data).delete()
    db.session.commit()
    return jsonify({'message': 'success'})

@app.route('/get_tags')
def get_tags():
    tags = Tag.query.all()
    return jsonify({"tags": [t.as_dict() for t in tags]})

if __name__ == '__main__':
    app.run(debug=True)