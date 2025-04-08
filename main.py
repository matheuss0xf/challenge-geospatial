from flask import Flask
from flask_restx import Api

from app.config import Config
from app.controllers.location import location_ns

api = Api(
    version='1.0',
    title='Location API',
    description='API for managing locations',
    doc='/api/v1/docs',
    prefix='/api/v1',
)


def create_app():
    app = Flask(__name__)
    api.init_app(app)

    api.add_namespace(location_ns, '/locations')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
