from peewee import Model
from playhouse.cockroachdb import DatabaseProxy

database = DatabaseProxy()

class BaseModel(Model):
    class Meta:
        database = database
