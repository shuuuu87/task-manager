from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Task

app = create_app()
migrate = Migrate(app, db)

# Optional: So you can access these models in `flask shell`
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task}

if __name__ == '__main__':
    app.run(debug=True)
