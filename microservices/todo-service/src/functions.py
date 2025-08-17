from datetime import datetime, timezone
from data_models.tag import Tag

def convert_date_string_to_datetime(data: any) -> datetime:
    # TODO fix the issue with the timezone conversion
    date_string = data["dueDate"] if "dueDate" in data else None
    if not date_string:
        return None
    try:
        return datetime.fromisoformat(date_string).astimezone(timezone.utc)
    except ValueError:
        return datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %Z')

def create_tag_objects(data):
    tags = data.pop("tags", [])
    tag_objects = []
    for tag in tags:
        tag_object = Tag.query.filter_by(name=tag['name']).first()
        if tag_object:
            tag_objects.append(tag_object)
    return tag_objects