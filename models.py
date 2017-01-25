from peewee import *
from datetime import datetime

DATABASE = MySQLDatabase('flaskAPI', host="localhost", user="root", passwd="")

class Course(Model):
    class Meta:
        database = DATABASE
        db_table = 'courses'

    title = CharField(unique=True, max_length=250)
    description = TextField()
    created_at = DateTimeField(default=datetime.now())

    def to_json(self):
        return {'id' : self.id, 'title' : self.title, 'description' : self.description}

def create_course():
    title = "Ejercicio Flask"
    description = "Ejercicio de flask"
    if not Course.select().where(Course.title == title):
        Course.create(title=title, description=description)

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Course], safe=True)
    create_course()
    DATABASE.close()
