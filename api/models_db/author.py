# data/models_db/author.py

from tortoise import fields
from tortoise.models import Model

class Author(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name
