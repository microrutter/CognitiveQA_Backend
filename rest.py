from flask import Flask, request
from flask_restful import Resource, Api
from database.sqlAlchemyConnection import Sqlconnection as sd


app = Flask(__name__)
api = Api(app)

"""
Global Functions
"""


"""
    Rest end points
"""


class get_cluster_label(Resource):
    def get(self):
        data = sd(dbname=request.args["project"])
        return data.select_dict_label(request.args["cluster"])


class drop_table(Resource):
    def post(self):
        data = sd(dbname=request.args["project"])
        data.drop_table(request.args["table"])

class averagetodo(Resource):
    def get(self):
        data = sd(dbname=request.args["project"])
        return data.select_average_todo()
    
class averageinprogress(Resource):
    def get(self):
        data = sd(dbname=request.args["project"])
        return data.select_average_inprogress()


class unique_labels(Resource):
    def get(self):
        data = sd(dbname=request.args["project"])
        return data.get_unique_labels()


class getpro(Resource):
    def get(self):
        data = sd(dbname="projects")
        return data.select_projects()


class setpro(Resource):
    def put(self):
        data = sd(dbname="projects")
        data.add_projects(request.args["project"], request.args["build"])
        
class getbuild(Resource):
    def get(self):
        data = sd(dbname="projects")
        return data.select_project_build(request.args["project"])
        
class updatepro(Resource):
    def put(self):
        data = sd(dbname="projects")
        data.update_project_build(request.args["build"], request.args["project"])

class get_kmeans_results(Resource):
    def get(self):
        data = sd(dbname=request.args["project"])
        return data.select_label_kmeans()


class put_cluster_dict(Resource):
    def put(self):
        data = sd(dbname=request.args["project"])
        data.fill_dict(request.args["label"], request.args["cluster"])
        
class put_month_todo(Resource):
    def put(self):
        data = sd(dbname=request.args["project"])
        data.insert_label_average_todo(request.args["month"], request.args["avg"], request.args["total"])
        
class put_month_inprogress(Resource):
    def put(self):
        data = sd(dbname=request.args["project"])
        data.insert_label_average_inprogress(request.args["month"], request.args["avg"], request.args["total"])


class get_cluster_label_all(Resource):
    def get(self):
        data = sd(dbname=request.args["project"])
        return data.select_dict_label_all()


class put_percent_cluster(Resource):
    def put(self):
        data = sd(dbname=request.args["project"])
        data.insert_label_per_k(request.args["label"], request.args["percent"])


class put_sprint_display(Resource):
    def put(self):
        data = sd(dbname=request.args["project"])
        data.insert_sprint_for_display(
            request.args["iss"],
            request.args["sum"],
            request.args["desc"],
            request.args["sumdesc"],
            request.args["label"],
        )


class put_sprint_teaching(Resource):
    def put(self):
        data = sd(dbname=request.args["project"])
        data.label_sprint_add_to_teaching(
            request.args["identifier"], request.args["label"]
        )
        
class put_user(Resource):
    def put(self):
        data = sd(dbname="jira_users")
        data.create_user(user=request.args["user"], password=request.args["password"])
        
class get_jira_user(Resource):
    def get(self):
        data = sd(dbname="jira_users")
        return data.select_jira_user(user=request.args["user"])
    
class get_jira_user_id(Resource):
    def get(self):
        data = sd(dbname="jira_users")
        return data.select_jira_user_id(user=request.args["id"])
    
class put_trello_key(Resource):
    def put(self):
        data = sd(dbname="jira_users")
        return data.update_user_trello_key(user=request.args["id"], key=request.args["key"])

class put_jira(Resource):
    def put(self):
        data = sd(dbname="jira_users")
        return data.update_user_jira(user=request.args["id"], base=request.args["base"], login=request.args["login"], token=request.args["token"])


"""
    Add end points to api
"""

api.add_resource(drop_table, "/drop")

api.add_resource(unique_labels, "/labels")

api.add_resource(getpro, "/projects")

api.add_resource(getbuild, "/build")

api.add_resource(setpro, "/add")

api.add_resource(updatepro, "/updateproject")

api.add_resource(put_month_todo, "/addmonthtodo")

api.add_resource(put_month_inprogress, "/addmonthinprogress")

api.add_resource(get_kmeans_results, "/results")

api.add_resource(averagetodo, "/averagetodo")

api.add_resource(averageinprogress, "/averageinprogress")

api.add_resource(put_cluster_dict, "/cluster")

api.add_resource(get_cluster_label, "/clusterlabel")

api.add_resource(get_cluster_label_all, "/clusterlabelall")

api.add_resource(put_percent_cluster, "/addpercent")

api.add_resource(put_sprint_display, "/addsprintdisplay")

api.add_resource(put_sprint_teaching, "/addsprintteach")

api.add_resource(put_user, "/jira/user/create")

api.add_resource(get_jira_user, "/jira/user/get")

api.add_resource(get_jira_user_id, "/jira/user/get/id")

api.add_resource(put_trello_key, "/jira/user/add/trello")

api.add_resource(put_jira, "/jira/user/add/jira")

if __name__ == "__main__":
    app.run(debug=True)
