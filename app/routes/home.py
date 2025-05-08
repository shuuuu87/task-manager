from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.models import db, Task, User
from datetime import datetime

home_bp = Blueprint('home', __name__)

# Home Page - Show Tasks, Add Task
@home_bp.route('/', methods=['GET', 'POST'])
def homepage():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.register'))

    user = User.query.get(user_id)
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('auth.register'))

    # Add Task
    if request.method == 'POST':
        task_title = request.form.get('task_title')
        work_time = request.form.get('work_time')

        if task_title and work_time:
            new_task = Task(
                title=task_title,
                work_time=int(work_time),
                user_id=user.id,
                date_created=datetime.utcnow().date()
            )
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully!', 'success')
            return redirect(url_for('home.homepage'))

    # Fetch today's tasks
    today = datetime.utcnow().date()
    tasks = Task.query.filter_by(user_id=user.id, date_created=today).all()

    return render_template('home.html', user=user, tasks=tasks)

# Complete a Task
@home_bp.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.register'))

    task = Task.query.get(task_id)
    if task and task.user_id == user_id and not task.is_completed:
        task.is_completed = True
        user = User.query.get(user_id)
        user.score += 2  # +10 points per completed task
        db.session.commit()
        flash('Task marked as completed!', 'success')

    return redirect(url_for('home.homepage'))

# Delete a Task
@home_bp.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.register'))

    task = Task.query.get(task_id)
    if task and task.user_id == user_id:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')

    return redirect(url_for('home.homepage'))
