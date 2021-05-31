from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

db = SQLAlchemy()

app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('db/pg_conf.py')
db.init_app(app)


class Writer(Resource):
    def get(self, id):
        sql = f"""SELECT json_build_object('author', json_agg(row_to_json("writers")), 'books', 
        (SELECT json_agg(row_to_json("books")) from "books" where "books".author_id = {id})) from "writers" where 
        writers.id = {id};"""
        json_str = []
        result = db.session.execute(sql)
        for r in result:
            json_str = jsonify(r[0])
        return json_str


api.add_resource(Writer, '/writers/<id>')

if __name__ == '__main__':
    print('Example links: '
          '\nhttp://127.0.0.1:5000/writers/1'
          '\nhttp://127.0.0.1:5000/writers/2')

    app.run()
