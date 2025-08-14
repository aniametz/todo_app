from datetime import datetime, timezone
from data_models.tag import Tag

def convert_iso_to_datetime(iso_str):
    # TODO fix the issue with the timezone conversion
    if iso_str:
        return datetime.fromisoformat(iso_str)
    return None

def create_tag_objects(data):
    tags = data.pop("tags", [])
    tag_objects = []
    for tag in tags:
        tag_object = Tag.query.filter_by(name=tag['name']).first()
        if tag_object:
            tag_objects.append(tag_object)
    return tag_objects