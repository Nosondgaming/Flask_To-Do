# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'description': task.description, 'created_at': task.created_at} for task in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(title=data['title'], description=data.get('description'))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id}), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.json
    task = Task.query.get_or_404(id)
    task.title = data['title']
    task.description = data.get('description')
    db.session.commit()
    return jsonify({'id': task.id})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'result': True})

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)

