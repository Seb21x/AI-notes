from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from transformers import pipeline

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(300), nullable=True)
    summary = db.Column(db.String(300), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return '<Note %r>' % self.id

classifier = pipeline("zero-shot-classification", model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli")
labels = ["Meetings", "Ideas", "Health", "Work", "Finance", "Education", "Shopping", "Others"]

def classify(note):
    result = classifier(note, candidate_labels=labels)
    return result["labels"][0]

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize(note):
    summary = summarizer(note, max_length=50, min_length=10, do_sample=False)
    return summary[0]["summary_text"]

@app.route('/', methods=['GET'])
def index():
    notes = Notes.query.order_by(Notes.date_created).all()
    return render_template('index.html', tasks=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    data = request.get_json()
    note_content = data.get('note')
    if not note_content:
        return jsonify({"No content in your note!"}), 400

    category = classify(note_content)
    summary = summarize(note_content)
    new_note = Notes(content=note_content, category=category, summary=summary)

    try:
        db.session.add(new_note)
        db.session.commit()
        return jsonify({"success": True})
    except:
        return jsonify({'There was a problem with adding your note.'}), 500

@app.route('/delete/<int:id>')
def delete(id):
    note_to_delete = Notes.query.get_or_404(id)
    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem with deleting your note."

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    note = Notes.query.get_or_404(id)
    if request.method == 'POST':
        note.content = request.form['note']
        note.category = request.form['category']
        note.summary = request.form['summary']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem with editing your note."
    else:
        return render_template('edit.html', task=note)

if __name__ == '__main__':
    app.run(debug=True)