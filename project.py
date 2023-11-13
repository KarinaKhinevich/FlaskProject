from app import app
from app.models import User, Post


#создаем контекст оболочки для flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
