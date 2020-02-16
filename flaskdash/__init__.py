import dash
from flask import Flask, request, redirect
from flask.helpers import get_root_path
from flask_login import login_required
from flask_migrate import Migrate

from flaskdash.models import db
from flaskdash.login import login_manager
from flaskdash.api.controllers import api
from flaskdash.authentication.controllers import authentication


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    #if app.config["ENV"] == "development":
    #    app.config["LOGIN_DISABLED"] = True

    from flaskdash.dashapp1.layout import layout as layout1
    from flaskdash.dashapp1.callbacks import register_callbacks as register_callbacks1
    register_dashapp(app, 'Dashapp 1','dashapp1',layout1,register_callbacks1)

    from flaskdash.dashapp2.layout import layout as layout2
    register_dashapp(app, 'Dashapp 2','dashapp2',layout2,None)


    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "authentication.login"

    app.register_blueprint(api, url_prefix="/")
    app.register_blueprint(authentication, url_prefix="/")

    @app.before_request
    def before_request():
        if not request.is_secure and app.env != "development":
            url = request.url.replace("http://", "https://", 1)
            code = 302  # permanent redirect
            return redirect(url, code=code)

    return app


def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun):
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dashapp = dash.Dash(__name__,
                           server=app,
                           url_base_pathname=f'/{base_pathname}/',
                           assets_folder=get_root_path(__name__) + f'/{base_pathname}/assets/',
                           meta_tags=[meta_viewport])

    with app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        if register_callbacks_fun:
            register_callbacks_fun(my_dashapp)
    _protect_dashviews(my_dashapp)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])