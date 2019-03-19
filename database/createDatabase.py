import sqlite3
import os


class database:
    def __init__(self, connection):
        self.connection = connection

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.connection)
            return conn
        except Exception as e:
            raise e
        return None

    """
        Initial creation of tables for specific project 
        data
    """

    def initial(self):
        try:
            db = self.create_connection()
            cursor = db.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS lcpa(identifier TEXT PRIMARY KEY, text TEXT, type TEXT, cluster TEXT)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS sprint(identifier TEXT PRIMARY KEY, text TEXT, type TEXT, cluster TEXT)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS labelBugPer(label TEXT PRIMARY KEY, percent TEXT)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS dictionary(label TEXT PRIMARY KEY, cluster TEXT)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS labelBugPerKmeans(label TEXT PRIMARY KEY, percent TEXT)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS sprintForDisplay(Issue TEXT PRIMARY KEY,"
                + " Summary TEXT, Description TEXT, SumDesc TEXT, label TEXT)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS sprintForTeaching(Issue TEXT PRIMARY KEY,"
                + " Summary TEXT, Description TEXT, label TEXT)"
            )
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    """
        Initial creation of table to hold list of projects
    """

    def projects(self):
        try:
            db = self.create_connection()
            cursor = db.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS pro(identifier TEXT PRIMARY KEY, text TEXT)"
            )
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    """
        Add project to project database
    """

    def add_projects(self, task):
        sql = " INSERT INTO pro(identifier,text) VALUES(?,?) "
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql, task)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    """
        Get list of projects
    """

    def select_projects(self):
        sql = "SELECT identifier FROM pro"
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            raise e
        finally:
            db.close()

    def drop(self):
        try:
            db = self.create_connection()
            cursor = db.cursor()
            cursor.execute("DROP TABLE IF EXISTS dictionary")
            cursor.execute("DROP TABLE IF EXISTS labelBugPerKmeans")
            cursor.execute("DROP TABLE IF EXISTS sprintForDisplay")
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS dictionary(label TEXT PRIMARY KEY, cluster TEXT)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS labelBugPerKmeans(label TEXT PRIMARY KEY, percent TEXT)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS sprintForDisplay(Issue TEXT PRIMARY KEY,"
                + " Summary TEXT, Description TEXT, SumDesc TEXT, label TEXT)"
            )
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def insert_task(self, task):
        sql = " INSERT INTO lcpa(identifier,text,type,cluster) VALUES(?,?,?,?) "
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql, task)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def insert_sprint(self, task):
        sql = " INSERT INTO sprint(identifier,text,type,cluster) VALUES(?,?,?,?) "
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql, task)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def insert_label_per(self, task):
        sql = " INSERT INTO labelBugPer(label,percent) VALUES(?,?) "
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql, task)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def insert_label_per_k(self, task):
        sql = " INSERT INTO labelBugPerKmeans(label,percent) VALUES(?,?) "
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql, task)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def insert_sprint_for_display(self, task):
        sql = " INSERT INTO sprintForDisplay(Issue, Summary, Description, SumDesc, label) VALUES(?,?,?,?,?) "
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql, task)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def insert_sprint_for_teaching(self, task):
        sql = " INSERT INTO sprintForTeaching(Issue, Summary, Description, label) VALUES(?,?,?,?) "
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql, task)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def select_label(self):
        sql = "SELECT * FROM labelBugPer"
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            raise e
        finally:
            db.close()

    def select_label_kmeans(self):
        sql = "SELECT * FROM labelBugPerKmeans"
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            raise e
        finally:
            db.close()

    def fillDict(self, task):
        sql = " INSERT INTO dictionary(label,cluster) VALUES(?,?) "
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql, task)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def selectDictLabel(self, cluster):
        sql = "SELECT label FROM dictionary WHERE cluster =?"
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql, (cluster,))
            return cur.fetchone()[0]
        except Exception as e:
            raise e
        finally:
            db.close()

    def selectDictLabelAll(self):
        sql = "SELECT label FROM dictionary"
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            raise e
        finally:
            db.close()

    def select_sprint_for_display(self):
        sql = " SELECT * FROM sprintForDisplay "
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            raise e
        finally:
            db.close()

    def select_description_sprint_for_display(self):
        sql = " SELECT * FROM sprintForDisplay "
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            raise e
        finally:
            db.close()

    def labelSprintAddToTeaching(self, identifier, label):
        sql = " SELECT Summary, Description FROM sprintForDisplay WHERE Issue=? "
        try:
            db = self.create_connection()
            if self.checkTeachingSprint(identifier, db):
                cur = db.cursor()
                cur.execute(sql, (identifier,))
                res = cur.fetchone()
                task = (identifier, res[0], res[1], label)
                self.insert_sprint_for_teaching(task)
        except Exception as e:
            raise e
        finally:
            db.close()

    def update_sprint_for_teaching(self, task):
        sql = " UPDATE sprintForTeaching SET label = ? WHERE Issue = ? "
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql, task)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def checkTeachingSprint(self, identifier, db):
        sql = " SELECT count(*) FROM sprintForTeaching WHERE Issue=? "
        try:
            cur = db.cursor()
            cur.execute(sql, (identifier,))
            res = cur.fetchone()
            print(res[0])
            if res[0] == 0:
                return True
            else:
                return False
        except Exception as e:
            raise e

    def getUnlabelledSprint(self):
        sql = ' SELECT * FROM sprintForTeaching WHERE label IS NULL OR label = "" '
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            raise e
        finally:
            db.close()

    def getUniqueLabels(self):
        sql = ' SELECT DISTINCT label FROM sprintForTeaching WHERE label IS NOT NULL OR label != "" '
        try:
            db = self.create_connection()
            cur = db.cursor()
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            raise e
        finally:
            db.close()
