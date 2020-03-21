import sqlite3
import os

def createDatabase():
    contains = False
    b = os.path.dirname(os.path.dirname(__file__))
    files = os.listdir(b)
    if 'Tasker.db' in files:
        contains = True
    
    if contains == False:
        try:
            conn = sqlite3.connect('Tasker.db')
            crsr = conn.cursor()
            crsr.execute("CREATE TABLE 'Stage' ('Project_id' TEXT,'name' TEXT,'desc' TEXT,'tasks' TEXT,'reward' INTEGER)")
            crsr.execute("CREATE TABLE 'Task' ('Project_id' TEXT,'Name' TEXT,'Description' TEXT,'Assignee' TEXT,'Deadline' TEXT)")
            crsr.execute("CREATE TABLE 'cred' ('username' TEXT,'password' TEXT,'full_name' TEXT)")
            crsr.execute("CREATE TABLE 'project' ('ProjectID' TEXT,'Name' TEXT,'Description' TEXT,'Deadline' DATE,'owner' TEXT,'team_member' TEXT)")
            print("DATABASE CREATED SUCCESSFULLY")
        except expression as identifier:
            print("FAILED IN CREATING DATABASE !!!")