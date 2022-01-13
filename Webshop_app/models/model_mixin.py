from Webshop_app.db import db


class MixinModel():
    # Save to database.
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Delete from database.
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    # Filter by ...
    def find_by_attribute(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()
