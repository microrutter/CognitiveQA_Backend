import simplejson
import pymongo
import json
from bson.json_util import dumps
from bson.objectid import ObjectId


# Table Names
SPRINT = "sprint"
DEFECTPERCENTAGE = "defectpercentage"
DICTIONARY = "dictionary"
KMEANSDEFECTPERCENTAGE = "kmeansdefper"
CURRENTWORK = "currentwork"
TEACHING = "teaching"
PROJECT = "project"
AVERAGETODO = "avetodo"
AVERAGEINPROGRESS = "aveinprog"
USER = "user"


class Sqlconnection:

    def __init__(self, dbname=""):
        mongo = pymongo.MongoClient("mongodb://172.17.0.4:27017/")
        self.db_engine = mongo[dbname]

    def drop_table(self, table_name: str):
        """
        Drops any given collection
        :Author: Wayne Rutter
        :Params: table_name String name of collection to be dropped
        """
        mycol = self.db_engine[table_name]
        mycol.drop()

    def add_projects(self, ident: str, desc: str):
        """
        Add project into project table and identify if it is building a model
        :Author: Wayne Rutter
        :Params: ident String project identifier
        :Params: desc String is the project creating a model or not
        """
        mycol = self.db_engine[PROJECT]
        mydict = { "identifier": ident, "model": desc }
        mycol.insert_one(mydict)
        
    def fill_dict(self, lab: str, clu: str):
        """
        Enter the label and the cluster the label belongs to
        :Author: Wayne Rutter
        :Params: lab String label of cluster
        :Params: clu String the number of the cluset
        """
        mycol = self.db_engine[DICTIONARY]
        mydict = {"label": lab, "cluster": clu}
        mycol.insert_one(mydict)

    def insert_label_per_k(self, lab: str, per: str):
        """
        Insert the percentage of bugs per cluster
        :Author: Wayne Rutter
        :Params: lab String label of cluster
        :Params: per String percentage of bugs
        """
        mycol = self.db_engine[KMEANSDEFECTPERCENTAGE]
        mydict = {"label": lab, "percentage": per}
        mycol.insert_one(mydict)
        
    def insert_label_average_todo(self, month: str, per: str, total: str):
        """
        Insert the monthly results for the average time that a 
        ticket took to go from start to done
        :Author: Wayne Rutter
        :Params: Month String the month of the result
        :Params: per String the average time
        :Params: total String the total number of tickets for each month
        """
        mycol = self.db_engine[AVERAGETODO]
        mydict = {"label": month, "average": per, "total": total}
        mycol.insert_one(mydict)
        
    def insert_label_average_inprogress(self, month: str, per: str, total: str):
        """
        Insert the monthly results for the average time that a 
        ticket took to go from In Progress to done
        :Author: Wayne Rutter
        :Params: Month String the month of the result
        :Params: per String the average time
        :Params: total String the total number of tickets for each month
        """
        mycol = self.db_engine[AVERAGEINPROGRESS]
        mydict = {"label": month, "average": per, "total": total}
        mycol.insert_one(mydict)

    def select_projects(self) -> dict:
        """
        Select all the current projects within the collection
        :Author: Wayne Rutter
        :Returns: dict
        """
        mycol = self.db_engine[PROJECT]
        return dumps(list(mycol.find()))
    
    def select_project_build(self, pro:str) -> dict:
        """
        Select the asked for project
        :Author: Wayne Rutter
        :Returns: dict
        """
        mycol = self.db_engine[PROJECT]
        myquery = { "identifier": pro }
        return dumps(list(mycol.find(myquery)))

    def select_label_kmeans(self) -> dict:
        """
        Select all from the bugs percentage collection
        :Author: Wayne Rutter
        :Returns: dict
        """
        mycol = self.db_engine[KMEANSDEFECTPERCENTAGE]
        return dumps(list(mycol.find()))

    def select_average_todo(self) -> dict:
        """
        Select all from the average todo table
        :Author: Wayne Rutter
        :Returns: dict
        """
        mycol = self.db_engine[AVERAGETODO]
        return dumps(list(mycol.find()))
    
    def select_average_inprogress(self) -> dict:
        """
        Select all from the average inprogress table
        :Author: Wayne Rutter
        :Returns: dict
        """
        mycol = self.db_engine[AVERAGEINPROGRESS]
        return dumps(list(mycol.find()))
    
    def select_dict_label_all(self):
        """
        Select all labels
        :Author: Wayne Rutter
        :Returns: dict
        """
        mycol = self.db_engine[DICTIONARY]
        return dumps(list(mycol.find()))

    def select_dict_label(self, cluster: str) -> dict:
        """
        Select a label given a cluster
        :Author: Wayne Rutter
        :Returns: dict
        """
        mycol = self.db_engine[DICTIONARY]
        myquery = { "cluster": cluster }
        return dumps(list(mycol.find(myquery)))

    def update_project_build(self, build: str, project: str):
        """
        Update the build state of a project
        :Author: Wayne Rutter
        :Params: build String build state 
        :Params: project String the project you want to change
        """
        mycol = self.db_engine[PROJECT]
        myquery = { "identifier": project }
        newvalues = { "$set": { "model": build } }
        mycol.update_one(myquery, newvalues)
        
    def create_jira_user(self, user:str, password:str, base:str, login:str, token:str):
        """
        Creates and stores a JIRA user in mongo
        :Author: Wayne Rutter
        :Params: user String username
        :Params: password String password
        :Params: base String url of JIRA server
        :Params: login String username of JIRA account
        :Params: token String access token for JIRA account
        """
        jira = {"base": base, "login": login, "token": token}
        mydict = {"user": user, "password": password, "jira": jira}
        mycol = self.db_engine[USER]
        mycol.insert_one(mydict)
        
    def select_jira_user(self, user:str):
        """
        Creates and stores a JIRA user in mongo
        :Author: Wayne Rutter
        :Params: user String username
        :Params: password String password
        """
        myquery = {"user": user}
        mycol = self.db_engine[USER]
        return dumps(list(mycol.find(myquery)))
    
    def select_jira_user_id(self, user:str):
        """
        Creates and stores a JIRA user in mongo
        :Author: Wayne Rutter
        :Params: user String username
        :Params: password String password
        """
        myquery = {"_id": ObjectId(user)}
        mycol = self.db_engine[USER]
        return dumps(list(mycol.find(myquery)))
        

