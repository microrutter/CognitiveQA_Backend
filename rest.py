from flask import Flask, request
from flask_restful import Resource, Api
from database.sqlAlchemyConnection import Sqlconnection as sd
import os



app = Flask(__name__)
api = Api(app)

'''
Global Functions
'''


'''
    Rest end points
'''
class label_teaching(Resource):

    def put(self, identifier):
        data = sd('sqlite', dbname=os.path.join(os.path.curdir, request.args['project'] + '.sqlite'))
        data.update_sprint_for_teaching(request.args['label'], identifier)

class create_db_tables(Resource):

    def get(self):
        data = sd('sqlite', dbname=os.path.join(os.path.curdir, request.args['project'] + '.sqlite'))
        data.create_db_tables()

class create_db_project(Resource):

    def get(self):
        data = sd('sqlite', dbname=os.path.join(os.path.curdir, 'projects.sqlite'))
        data.projects()


class sprint_display(Resource):

    def get(self):
        data = sd('sqlite', dbname=os.path.join(os.path.curdir, request.args['project'] + '.sqlite'))
        return data.select_sprint_for_display()

class drop_table(Resource):

    def post(self):
        data = sd('sqlite', dbname=os.path.join(os.path.curdir, request.args['project'] + '.sqlite'))
        data.drop_table(request.args['table'])

class unlabeled(Resource):

    def get(self):
        data = sd('sqlite', dbname=os.path.join(os.path.curdir, request.args['project'] + '.sqlite'))
        return data.get_un_labelled_sprint()

class unique_labels(Resource):

    def get(self):
        data = sd('sqlite', dbname=os.path.join(os.path.curdir, request.args['project'] + '.sqlite'))
        return data.get_unique_labels()

class getpro(Resource):

    def get(self):
        data = sd('sqllite', dbname=os.path.join(os.path.curdir, 'projects.sqlite'))
        return data.select_projects()

class setpro(Resource):

    def put(self):
        print(request.args['project'])
        print(request.args['description'])
        data = sd('sqllite', dbname=os.path.join(os.path.curdir, 'projects.sqlite'))
        data.add_projects(request.args['project'], request.args['description'])



'''
    Add end points to api
'''
api.add_resource(label_teaching, '/teaching/<identifier>')

api.add_resource(create_db_tables, '/create')

api.add_resource(create_db_project, '/createproject')

api.add_resource(sprint_display, '/sprint')

api.add_resource(drop_table, '/drop')

api.add_resource(unlabeled, '/trainsprint')

api.add_resource(unique_labels, '/labels')

api.add_resource(getpro, '/projects')

api.add_resource(setpro, '/add')

if __name__ == '__main__':
    app.run(debug=True)
