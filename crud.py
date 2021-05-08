"""Create, read, update and delete"""

def create_image_path(username, image):
    """Add a new image into BD into Chat TB"""
    new_image = Chat(username=username, image=image)
    db.session.add(user)
    db.session.commit()

    return new_image
