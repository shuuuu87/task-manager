from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Task

app = create_app()
migrate = Migrate(app, db)

# Optional: Helps with flask shell usage
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task}

# This block is safe for local dev; Render will ignore it
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
