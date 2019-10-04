from flask import Flask, request
from flask_restful import Resource, Api
from database.sqlAlchemyConnection import Sqlconnection as sd
import os


app = Flask(__name__)
api = Api(app)

"""
Global Functions
"""


"""
    Rest end points
"""


class label_teaching(Resource):
    def put(self, identifier):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        data.update_sprint_for_teaching(request.args["label"], identifier)


class create_db_tables(Resource):
    def get(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        data.create_db_tables()


class create_db_project(Resource):
    def get(self):
        data = sd("sqlite", dbname=os.path.join(os.path.curdir, "projects.sqlite"))
        data.projects()


class sprint_display(Resource):
    def get(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        return data.select_sprint_for_display()


class get_cluster_label(Resource):
    def get(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        return data.select_dict_label(request.args["cluster"])


class drop_table(Resource):
    def post(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        data.drop_table(request.args["table"])


class unlabeled(Resource):
    def get(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        return data.get_un_labelled_sprint()

class average(Resource):
    def get(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        return data.select_average()


class unique_labels(Resource):
    def get(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        return data.get_unique_labels()


class getpro(Resource):
    def get(self):
        data = sd("sqlite", dbname=os.path.join(os.path.curdir, "projects.sqlite"))
        return data.select_projects()


class setpro(Resource):
    def put(self):
        data = sd("sqlite", dbname=os.path.join(os.path.curdir, "projects.sqlite"))
        data.add_projects(request.args["project"], request.args["build"])
        
class getbuild(Resource):
    def get(self):
        data = sd("sqlite", dbname=os.path.join(os.path.curdir, "projects.sqlite"))
        return data.select_project_build(request.args["project"])
        
class updatepro(Resource):
    def put(self):
        data = sd("sqlite", dbname=os.path.join(os.path.curdir, "projects.sqlite"))
        data.update_project_build(request.args["build"], request.args["project"])

class get_kmeans_results(Resource):
    def get(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        return data.select_label_kmeans()


class put_cluster_dict(Resource):
    def put(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        data.fill_dict(request.args["label"], request.args["cluster"])
        
class put_month(Resource):
    def put(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        data.insert_label_average(request.args["month"], request.args["avg"], request.args["total"])


class get_cluster_label_all(Resource):
    def get(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        return data.select_dict_label_all()


class put_percent_cluster(Resource):
    def put(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        data.insert_label_per_k(request.args["label"], request.args["percent"])


class put_sprint_display(Resource):
    def put(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        data.insert_sprint_for_display(
            request.args["iss"],
            request.args["sum"],
            request.args["desc"],
            request.args["sumdesc"],
            request.args["label"],
        )


class put_sprint_teaching(Resource):
    def put(self):
        data = sd(
            "sqlite",
            dbname=os.path.join(os.path.curdir, request.args["project"] + ".sqlite"),
        )
        data.label_sprint_add_to_teaching(
            request.args["identifier"], request.args["label"]
        )


"""
    Add end points to api
"""
api.add_resource(label_teaching, "/teaching/<identifier>")

api.add_resource(create_db_tables, "/create")

api.add_resource(create_db_project, "/createproject")

api.add_resource(sprint_display, "/sprint")

api.add_resource(drop_table, "/drop")

api.add_resource(unlabeled, "/trainsprint")

api.add_resource(unique_labels, "/labels")

api.add_resource(getpro, "/projects")

api.add_resource(getbuild, "/build")

api.add_resource(setpro, "/add")

api.add_resource(updatepro, "/updateproject")

api.add_resource(put_month, "/addmonth")

api.add_resource(get_kmeans_results, "/results")

api.add_resource(average, "/average")

api.add_resource(put_cluster_dict, "/cluster")

api.add_resource(get_cluster_label, "/clusterlabel")

api.add_resource(get_cluster_label_all, "/clusterlabelall")

api.add_resource(put_percent_cluster, "/addpercent")

api.add_resource(put_sprint_display, "/addsprintdisplay")

api.add_resource(put_sprint_teaching, "/addsprintteach")

if __name__ == "__main__":
    app.run(debug=True)
