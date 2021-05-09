"""Create, read, update and delete"""
from model import * 

def add_image_path(complete_path):
    """Add a new image into BD into Chat TB

    >>> add_image_path("./static/images/testing.png")
    <Chat id:1 image_path:./static/images/testing.png>
    
    """
    new_image = Chat(image_path=complete_path)
    db.session.add(new_image)
    db.session.commit()

    return new_image


def pull_latest_images():
    """Get the images to render on homepage"""
    try: 
        imgs = Chat.query.order_by(Chat.id.asc()).all()
        return imgs
    except:
        pass


if __name__ == '__main__':
    from server import app
    connect_to_db(app)