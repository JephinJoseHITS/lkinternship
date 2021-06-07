from flask import Flask, request, g
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# DATABASE = 'sqlite:///database.db'


# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db

# db = get_db()

todos = {'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'}}


class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(100), nullable = False)
    due_by = db.Column(db.String(10), nullable = False)
    status = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return id

todo_put_args = reqparse.RequestParser()
todo_put_args.add_argument("task", type=str, help="Name of the task is required", required=True)
todo_put_args.add_argument("due_by", type=str, help="Due by date", required=True)
todo_put_args.add_argument("status", type=str, help="Status of task", required=True)

todo_update_args = reqparse.RequestParser()
todo_update_args.add_argument("task", type=str, help="Name of the task is required")
todo_update_args.add_argument("due_by", type=int, help="Due by date")
todo_update_args.add_argument("status", type=int, help="Status of task")

resource_fields = {
    'due_by': fields.String,
    'status': fields.String
}


class Todo(Resource):
	@marshal_with(resource_fields)
	def get(self, todo_id):
		result = TodoModel.query.filter_by(id=todo_id).first()
		if not result:
			abort(404, message="Could not find task with that id")
		return result

	@marshal_with(resource_fields)
	def put(self, todo_id):
		args = todo_put_args.parse_args()
		result = TodoModel.query.filter_by(id=todo_id).first()
		if result:
			abort(409, message="Task id taken...")

		todo = TodoModel(id=todo_id, name=args['task'], due_by=args['due_by'], status=args['status'])
		db.session.add(todo)
		db.session.commit()
		return todo, 201


	@marshal_with(resource_fields)
	def patch(self, todo_id):
		args = todo_update_args.parse_args()
		result = TodoModel.query.filter_by(id=todo_id).first()
		if not result:
			abort(404, message="Video doesn't exist, cannot update")

		if args['task']:
			result.name = args['task']
		if args['due_by']:
			result.views = args['due_by']
		if args['status']:
			result.likes = args['status']

		db.session.commit()

		return result

	def delete(self, todo_id):
		del todos[todo_id]
		return '', 204


api.add_resource(Todo, "/todo/<int:todo_id>")



if __name__ == '__main__':
    app.run(debug=True)