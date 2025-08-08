from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_migrate import Migrate

from data_models.todo import Todo
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
    new_todo = Todo(**data)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'success'})

@app.route('/update_todo', methods=["POST"])
def update_todo():
    data = request.get_json().get("todoData")
    data["completedAt"] = datetime.now(timezone.utc) if data["isDone"] else None
    # TODO: find a way to resolve this issue with datetime format from svelte
    del data["createdAt"]  # createdAt should not be updated because its fromat from svelte is not compatible with the database
    Todo.query.filter_by(id=data["id"]).update(data)
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

if __name__ == '__main__':
    app.run(debug=True)