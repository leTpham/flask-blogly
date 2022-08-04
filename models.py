"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


DEFAULT_IMAGE_URL = "https://static.independent.co.uk/2021/12/03/15/Pisco%20Cat%20puss%20in%20boots-1.jpg?width=1200"


class User(db.Model):
    """Pet."""

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
                    default = DEFAULT_IMAGE_URL) #maybe DEFAULT here??


    # def greet(self):
    #     """Greet using name."""

    #     return f"I'm {self.name} the {self.species or 'thing'}"

    # def feed(self, units=10):
    #     """Nom nom nom."""

    #     self.hunger -= units
    #     self.hunger = max(self.hunger, 0)

    # @classmethod
    # def get_by_species(cls, species):
    #     """Get all pets matching that species."""

    #     return cls.query.filter_by(species=species).all()
