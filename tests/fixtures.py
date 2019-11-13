import pytest
from flask import Flask
from flask_jwt_router.JwtRoutes import JwtRoutes

app = Flask(__name__)


@app.route("/test", methods=["GET"])
def test_one():
    return "/test"


@pytest.fixture(scope="function")
def jwt_router_client(request):
    app.config = {**app.config, **request.param}
    JwtRoutes(app)
    app.config["TESTING"] = True
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()


flask_app = Flask(__name__)


@flask_app.route("/api/v1/test", methods=["GET"])
def test_two():
    return "/test"


@flask_app.route("/api/v1/bananas/sub", methods=["GET"])
def test_sub():
    return {"data": "sub"}, 200


@flask_app.route("/api/v1/test/sub_two", methods=["GET"])
def test_sub_two():
    return {"data": "sub2"}, 200


@flask_app.route("/api/v1/apples/sub/<int:user_id>", methods=["GET"])
def test_sub_three(user_id=1):
    return {"data": user_id}, 200


@pytest.fixture(scope='module')
def test_client():
    flask_app.config["WHITE_LIST_ROUTES"] = [
        ("GET", "/test"),
        ("GET", "/bananas/sub"),
        ("GET", "/apples/sub/<int:user_id>")
    ]
    flask_app.config["JWT_ROUTER_API_NAME"] = "/api/v1"
    JwtRoutes(flask_app)
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture(scope='module')
def test_client_static():
    flask_app_static = Flask(__name__, static_folder="static_copy")
    flask_app_static.config["WHITE_LIST_ROUTES"] = [("GET", "/anything")]
    JwtRoutes(flask_app_static)
    testing_client = flask_app_static.test_client()
    ctx = flask_app_static.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()
