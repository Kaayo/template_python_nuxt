# data/models_db/todo.py

from tortoise import fields
from tortoise.models import Model
from models_db.author import Author  # Importar o modelo Author

class Todo(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=255)
    completed = fields.BooleanField(default=False)

    # Relacionamento com Author (um para muitos)
    author = fields.ForeignKeyField('models_db.Author', related_name='todos')

    def __str__(self):
        return self.description
