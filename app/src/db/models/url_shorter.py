from tortoise import fields, models


class URLInfo(models.Model):
    id = fields.IntField(pk=True)
    link = fields.CharField(max_length=100)
    original_link = fields.TextField()
    is_active = fields.BooleanField(default=True)
    due_date = fields.DatetimeField()


class URLRedirect(models.Model):
    id = fields.IntField(pk=True)
    url = fields.ForeignKeyField("models.URLInfo", related_name="clicks", on_delete=fields.CASCADE)
    clicked_at = fields.DatetimeField(auto_now_add=True)
