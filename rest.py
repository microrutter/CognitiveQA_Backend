from flask import Flask, request
from flask_restful import Resource, Api
from database.sqlAlchemyConnection import Sqlconnection as sd
from model.heatmap import heatmap as h
from model.training import trainModel as tm
from transform.ProcessInformation import DataTransform as jt
from externaldata.jiraTransformData import JiraTransform as j
import os



app = Flask(__name__)
api = Api(app)

'''
Global Functions
'''

'''
Function to add data to database and train cluster model
'''
def addingData(data, teach, cluster):
    test = j(_URL_, _PROJECT_, _USERNAME_, _PASSWORD_)
    trans = jt()
    sprint = test.tran_data(whi='backlog')
    teach.save(teach.train(sprint['Cleaned_cluster'], cluster))
    teach.labelDatabase(data)
    h.createKmeansHeatMap(h, sprint, teach, data)
    sp = test.tran_data(whi='sprint')
    trans.getRelatedStories(sprint, sp)
    h.createLabelSprint(h, sp, data, teach)


'''
    Rest end points
'''
class label(Resource):

    def put(self, identifier):
        data = sd('sqlite', dbname=os.path.join(os.path.curdir, request.args['project'] + '.sqlite'))
        data.update_sprint_for_teaching(request.args['label'], identifier)

class heatmapKmeans(Resource):

    def get(self):
        """
        if os.path.isfile(os.path.join(os.path.curdir, request.args['project'] + '.sqlite')):
            data = sd('sqlite', dbname=os.path.join(os.path.curdir, request.args['project'] + '.sqlite'))
            return data.select_label_kmeans()
        else:"""
        data = sd('sqlite', dbname=os.path.join(os.path.curdir, request.args['project'] + '.sqlite'))
        data.create_db_tables()
        teach = tm(request.args['project'])
        addingData(data, teach, 8)
        return data.select_label_kmeans()

class sprint(Resource):

    def get(self):
        data = sd('sqlite', dbname=os.path.join(os.path.curdir, request.args['project'] + '.sqlite'))
        return data.select_sprint_for_display()

class reload(Resource):

    def post(self):
        data = sd('sqlite', dbname=os.path.join(os.path.curdir, request.args['project'] + '.sqlite'))
        teach = tm(request.args['project'])
        data.drop()
        addingData(data, teach, int(request.args['cluster']))
        return True

class relabel(Resource):

    def get(self):
        data = sd('sqlite', dbname=os.path.join(os.path.curdir, request.args['project'] + '.sqlite'))
        return data.get_un_labelled_sprint()

class labels(Resource):

    def get(self):
        data = sd('sqlite', dbname=os.path.join(os.path.curdir, request.args['project'] + '.sqlite'))
        return data.get_unique_labels()

class getpro(Resource):

    def get(self):
        data = sd('sqllite', dbname=os.path.join(os.path.curdir, 'projects.sqlite'))
        data.projects()
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
api.add_resource(label, '/label/<identifier>')

api.add_resource(heatmapKmeans, '/kmeans')

api.add_resource(sprint, '/sprint')

api.add_resource(reload, '/retrain')

api.add_resource(relabel, '/relabel')

api.add_resource(labels, '/labels')

api.add_resource(getpro, '/projects')

api.add_resource(setpro, '/add')

if __name__ == '__main__':
    app.run(debug=True)
