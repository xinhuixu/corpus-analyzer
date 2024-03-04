# Define database models
from extensions import db

class Transcript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    transcript_data = db.Column(db.JSON, nullable=True)
    speakers = db.Column(db.JSON, nullable=True)  # Store list of unique speakers
    airtimes = db.Column(db.JSON, nullable=True)  # Store airtime data
    airtimes_chart_path = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Transcript {self.filename}>'
