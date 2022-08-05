"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


DEFAULT_IMAGE_URL = "https://static.independent.co.uk/2021/12/03/15/Pisco%20Cat%20puss%20in%20boots-1.jpg?width=1200"


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable=False)
    image_url = db.Column(db.Text,
                    nullable=True,
                    default = DEFAULT_IMAGE_URL)
    user_posts = db.relationship('Post', backref = 'user')

class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                     nullable=False)
    content = db.Column(db.Text,
                     nullable=False)
    created_at = db.Column(db.DateTime,
                     nullable=False,
                    default=db.func.now())
    user_id = db.Column(db.Integer,
                     db.ForeignKey('users.id'),
                      nullable=False,)
    tag_post = db.relationship('Tag',
                               secondary='posts_tags',
                               backref='posts')


class Tag(db.Model):
    """Tag"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String(50),
                    nullable= False)


class PostTag(db.Model):
        __tablename__ = "posts_tags"

        post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
        tag_id = db.Column(db.Integer,
                            db.ForeignKey("tags.id"),
                            primary_key=True)

