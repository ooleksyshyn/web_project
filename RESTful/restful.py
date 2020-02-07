from src.app import api
from flask_restful import Resource


class HelloWorld(Resource):
    def get(self):
        return {"Hello": "World"}, 200


api.add_resource(HelloWorld, "/")
