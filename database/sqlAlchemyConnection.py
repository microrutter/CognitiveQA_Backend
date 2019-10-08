from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, REAL
from sqlalchemy.ext.declarative import declarative_base
import simplejson

# Global Variables
SQLITE = "sqlite"

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


class Sqlconnection:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {SQLITE: "sqlite:///{DB}"}

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, username="", password="", dbname=""):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    """
        Create Tables for database main project
    """
    def create_db_tables(self):
        metadata = MetaData()
        sprint = Table(
            SPRINT,
            metadata,
            Column("identifier", String, primary_key=True),
            Column("text", String),
            Column("type", String),
            Column("cluster", String),
        )
        defper = Table(
            DEFECTPERCENTAGE,
            metadata,
            Column("label", String, primary_key=True),
            Column("percent", String),
        )
        averagetodo = Table(
            AVERAGETODO,
            metadata,
            Column("label", String, primary_key=True),
            Column("average", String),
            Column("total", String),
        )
        averageinprogress = Table(
            AVERAGEINPROGRESS,
            metadata,
            Column("label", String, primary_key=True),
            Column("average", String),
            Column("total", String),
        )
        dictionary = Table(
            DICTIONARY,
            metadata,
            Column("label", String, primary_key=True),
            Column("cluster", String),
        )
        kmeansdefper = Table(
            KMEANSDEFECTPERCENTAGE,
            metadata,
            Column("label", String, primary_key=True),
            Column("percentage", String),
        )
        currentwork = Table(
            CURRENTWORK,
            metadata,
            Column("Issue", String, primary_key=True),
            Column("Summary", String),
            Column("Description", String),
            Column("SumDesc", String),
            Column("label", String),
        )
        teaching = Table(
            TEACHING,
            metadata,
            Column("Issue", String, primary_key=True),
            Column("Summary", String),
            Column("Description", String),
            Column("SumDesc", String),
            Column("label", String),
        )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    """
        Create Tables project database
    """
    def projects(self):
        metadata = MetaData()
        project = Table(
            PROJECT,
            metadata,
            Column("identifier", String, primary_key=True),
            Column("model", String),
        )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    """
        Drop any given table
    """
    def drop_table(self, table_name):
        base = declarative_base()
        metadata = MetaData(self.db_engine, reflect=True)
        table = metadata.tables.get(table_name)
        if table is not None:
            print(f"Deleting {table_name} table")
            base.metadata.drop_all(self.db_engine, [table], checkfirst=True)

    """
        Insert, Update, Delete query processor
    """
    def execute_query(self, query=""):
        if query == "":
            return
        print(query)

        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
                jsonstring = []
                for r in result:
                    js = []
                    for e in r:
                        js.append(e)
                    jsonstring.append(js)
                return jsonstring
            except Exception as e:
                print(e)

    """
        Insert project to project database
    """
    def add_projects(self, ident, desc):
        # Insert Data
        query = "INSERT INTO {TBL_USR}(identifier,model) " \
                "VALUES({ID}, {TEX});".format(TBL_USR=PROJECT, ID="\"" + ident + "\"", TEX="\"" + desc + "\"")
        self.execute_query(query)

    """
        Insert data into dictionary for cluster labels
    """
    def fill_dict(self, lab, clu):
        query = "INSERT INTO {TBL_USR}(label,cluster) " \
                "VALUES({LAB},{CLU})".format(TBL_USR=DICTIONARY, LAB="\"" + lab + "\"", CLU="\"" + clu + "\"")
        self.execute_query(query)

    """
        Insert percentage for clustering defects
    """
    def insert_label_per_k(self, lab, per):
        query = "INSERT INTO {TBL_USR}(label,percentage) " \
                "VALUES({LAB},{PER})".format(TBL_USR=KMEANSDEFECTPERCENTAGE, LAB="\"" + lab + "\"", PER="\"" + per + "\"")
        self.execute_query(query)
        
    """
        Insert average todo
    """
    def insert_label_average_todo(self, month,per,total):
        query = "INSERT INTO {TBL_USR}(label,average,total) " \
                "VALUES({LAB},{PER},{TOT})".format(TBL_USR=AVERAGETODO, LAB="\"" + month + "\"", PER="\"" + per + "\"", TOT="\"" + total + "\"")
        self.execute_query(query)
        
    """
        Insert average in progress
    """
    def insert_label_average_inprogress(self, month,per,total):
        query = "INSERT INTO {TBL_USR}(label,average,total) " \
                "VALUES({LAB},{PER},{TOT})".format(TBL_USR=AVERAGEINPROGRESS, LAB="\"" + month + "\"", PER="\"" + per + "\"", TOT="\"" + total + "\"")
        self.execute_query(query)

    """
        Insert sprint data in for display
    """
    def insert_sprint_for_display(self, iss, sum, desc, sumdesc, lab):
        query = "INSERT INTO " \
                "{TBL_USR}(Issue, Summary, Description, SumDesc, label) " \
                "VALUES({ISS},{SUM},{DESC},{SUMDESC},{LAB})".format(TBL_USR=CURRENTWORK,
                                                                    ISS="\"" + iss + "\"",
                                                                    SUM="\"" + sum + "\"",
                                                                    DESC="\"" + desc + "\"",
                                                                    SUMDESC="\"" + sumdesc + "\"",
                                                                    LAB="\"" + lab + "\"")
        self.execute_query(query)

    """
        Insert data into teaching table
    """
    def insert_sprint_for_teaching(self, iss, sum, desc, lab):
        query = "INSERT INTO {TBL_USR}(Issue, Summary, Description, label) " \
                "VALUES({ISS},{SUM},{DESC},{LAB})".format(TBL_USR=TEACHING,
                                                          ISS="\"" + iss + "\"",
                                                          SUM="\"" + sum + "\"",
                                                          DESC="\"" + desc + "\"",
                                                          LAB="\"" + lab + "\"")
        self.execute_query(query)

    """
        Lable sprint and add it to teaching database
    """
    def label_sprint_add_to_teaching(self, identifier, label):
        query = "SELECT Summary, Description " \
                "FROM {TBL_USR} " \
                "WHERE Issue={IDENT}".format(TBL_USR=CURRENTWORK,
                                             IDENT=identifier)

        count = "SELECT count(*) " \
                "FROM {TBL_USR} " \
                "WHERE Issue={IDENT}".format(TBL_USR=TEACHING,
                                             IDENT=identifier)

        if self.execute_query(count):
            res = self.execute_query(query)
            self.insert_sprint_for_teaching(identifier, res[0], res[1], label)


    """
        Select all available projects
    """
    def select_projects(self):
        query = "SELECT identifier FROM {TBL_USR}".format(TBL_USR=PROJECT)
        return self.execute_query(query)
    
    """
        Select all available projects
    """
    def select_project_build(self, pro:str):
        query = "SELECT model " \
                "FROM {TBL_USR} " \
                "WHERE identifier={project}".format(TBL_USR=PROJECT, project="\"" + pro + "\"")
        return self.execute_query(query)

    """
        Selects the clustering results from the table
    """
    def select_label_kmeans(self):
        query = "SELECT * FROM {TBL_USR}".format(TBL_USR=KMEANSDEFECTPERCENTAGE)
        return self.execute_query(query)

    """
        Select all from the average todo table
    """
    def select_average_todo(self):
        query = "SELECT * FROM {TBL_USR}".format(TBL_USR=AVERAGETODO)
        return self.execute_query(query)
    
    """
        Select all from the average inprogress table
    """
    def select_average_inprogress(self):
        query = "SELECT * FROM {TBL_USR}".format(TBL_USR=AVERAGEINPROGRESS)
        return self.execute_query(query)

    """
        Selects all the clustering labels
    """
    def select_dict_label_all(self):
        query = "SELECT label FROM {TBL_USR}".format(TBL_USR=DICTIONARY)
        return self.execute_query(query)

    """
        Selects one label given a cluster
    """
    def select_dict_label(self, cluster):
        query = "SELECT label FROM {TBL_USR} WHERE cluster = {CLU}".format(TBL_USR=DICTIONARY, CLU=cluster)
        return self.execute_query(query)

    """
        Select all data from current work database
    """
    def select_sprint_for_display(self):
        query = "SELECT * " \
                "FROM {TBL_USR}".format(TBL_USR=CURRENTWORK)
        return self.execute_query(query)

    """
        Select all data from teaching table_name
    """
    def get_un_labelled_sprint(self):
        query = "SELECT * " \
                "FROM {TBL_USR} " \
                "WHERE label IS NULL " \
                "OR label = ''".format(TBL_USR=TEACHING)
        return self.execute_query(query)

    def get_unique_labels(self):
        query = "SELECT DISTINCT label " \
                "FROM {TBL_USR} " \
                "WHERE label IS NOT NULL " \
                "OR label != ''".format(TBL_USR=TEACHING)
        return self.execute_query(query)

    """
        Update teaching database
    """
    def update_sprint_for_teaching(self, lab, iss):
        query = "UPDATE {TBL_USR} " \
                "SET label = {LAB} " \
                "WHERE Issue = {ISS}".format(TBL_USR=TEACHING,
                                             LAB=lab,
                                             ISS=iss)
        self.execute_query(query)
        
    """
        Update teaching database
    """
    def update_project_build(self, build, project):
        query = "UPDATE {TBL_USR} " \
                "SET model = {BUILD} " \
                "WHERE Identifier = {ISS}".format(TBL_USR=PROJECT,
                                             BUILD="\"" + build + "\"",
                                             ISS="\"" + project + "\"")
        self.execute_query(query)
