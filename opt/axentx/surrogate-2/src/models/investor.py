from . import db

class Investor(db.Model):
    __tablename__ = 'investors'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    firm_name = db.Column(db.String(120), nullable=False)
    investment_stage = db.Column(db.String(120), nullable=False)
    ticket_size = db.Column(db.String(120), nullable=False)
    focus_areas = db.Column(db.String(120), nullable=False)
    geographic_preference = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Investor {self.email}>'