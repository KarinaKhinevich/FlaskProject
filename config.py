import os

basedir=os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False #отключает ф-ю Flask-SQLAlchemy, которая будет сигнализировать приложению каждый раз, когда в БД должно быть внесено изменение
    SECRET_KEY = os.environ.get('SECRET_KEY') or "Deeargreendeer"
    #SECRET_KEY создает ключ из окружения или использует готовый от CSRF атак