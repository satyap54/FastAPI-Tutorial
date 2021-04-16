from tortoise import fields, models

class Todo(models.Model):
    id = fields.IntField(pk=True)
    todo = fields.CharField(max_length=250)
    due_date = fields.DateField(auto_now=False, auto_now_add=False)
