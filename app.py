from flask import Flask
import config
from exts import db,mail

from apps.cms.views import bp as cms_bp
from apps.common.views import bp as common_bp
from apps.front.views import bp as front_bp
from apps.ueditor.ueditor import bp as ueditor_bp
from flask_wtf import CSRFProtect


def create_app():
    app = Flask(__name__)
    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(ueditor_bp)

    app.config.from_object(config)
    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)

    return app

app=create_app()

if __name__ == '__main__':
    app=create_app()
    app.run(port=80,host="0.0.0.0")
