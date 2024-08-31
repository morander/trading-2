from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app import db
from app.models import Task

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/tasks')
def get_tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@bp.route('/tasks', methods=['POST'])
def create_task():
    title = request.form.get('title')
    description = request.form.get('description')
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('main.get_tasks'))

@bp.route('/tasks/<int:task_id>/edit', methods=['GET'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('edit_task.html', task=task)

@bp.route('/tasks/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.title = request.form.get('title')
    task.description = request.form.get('description')
    task.completed = 'completed' in request.form
    db.session.commit()
    return redirect(url_for('main.get_tasks'))

@bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.get_tasks'))

# API routes
@bp.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@bp.route('/api/tasks', methods=['POST'])
def api_create_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data.get('description', ''))
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@bp.route('/api/tasks/<int:task_id>', methods=['GET'])
def api_get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify(task.to_dict())

@bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204