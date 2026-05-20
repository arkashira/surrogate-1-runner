class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    # add any fields you need (e.g., email, password_hash)