from data_models.tag import Tag

def hamming_distance(chain1, chain2):
    return sum(c1 != c2 for c1, c2 in zip(chain1, chain2))

def create_tag_objects(data):
    tags = data.pop("tags", [])
    tag_objects = []
    for tag in tags:
        tag_object = Tag.query.filter_by(name=tag['name']).first()
        if tag_object:
            tag_objects.append(tag_object)
    return tag_objects