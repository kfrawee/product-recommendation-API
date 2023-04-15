import app
from config import is_dev

if __name__ == "__main__":
    if is_dev():
        db = app.db
        db.session.remove()
        db.drop_all(app=app.app)
