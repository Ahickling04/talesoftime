"""
app.py - Flask application factory for Tales of Time (raw SQL version).

SQLAlchemy is no longer used. Database initialisation is handled by
models.init_db(), which runs the raw DDL schema script.
"""
import os
from flask import Flask
from extensions import db
from models.models import Character, Item, Quest # Import your models here!

def create_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="static"
    )
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "tales-of-time-dev-key")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tales_of_time.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app) # Links the db instance to this app
    
    from views.views import bp
    
    app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
