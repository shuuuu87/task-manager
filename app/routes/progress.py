from flask import Blueprint, render_template, session
from app.models import Task, User
from datetime import datetime, timedelta
from sqlalchemy import func

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/progress')
def progress():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    today = datetime.utcnow().date()
    past_7_days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    
    daily_counts = {str(day): 0 for day in past_7_days}

    task_counts = (
        Task.query.with_entities(func.date(Task.date_created), func.count())
        .filter(Task.user_id == user_id, Task.is_completed == True, Task.date_created >= today - timedelta(days=6))
        .group_by(func.date(Task.date_created))
        .all()
    )

    for date_created, count in task_counts:
        date_str = str(date_created)
        if date_str in daily_counts:
            daily_counts[date_str] = count

    return render_template('progress.html', daily_counts=daily_counts)
