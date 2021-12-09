from tortoise import fields, models


class Tag(models.Model):
    name = fields.CharField(max_length=50, null=True)
    slug = fields.CharField(max_length=50, null=True)


class Category(models.Model):
    name = fields.CharField(max_length=48, null=True)
    slug = fields.CharField(max_length=50, null=True)


class User(models.Model):
    username = fields.CharField(max_length=24, unique=True)
    password_hash = fields.CharField(max_length=128, null=True)
    email = fields.CharField(max_length=60, null=True, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'userin'


class Post(models.Model):
    title = fields.CharField(max_length=55, null=True)
    slug = fields.CharField(max_length=35, null=True)
    category = fields.ManyToManyField('models.Category', related_name='category')
    tag = fields.ManyToManyField('models.Tag', related_name='tags')
    author = fields.ForeignKeyField('models.User', related_name='events')
    content = fields.CharField(max_length=150, null=True)
    image = fields.CharField(null=True, max_length=120)
    publish_date = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now_add=True)
    logged_only = fields.BooleanField()

    @property
    def categories_id(self):
        return [one_category.id for one_category in self.category]

    @property
    def tags_id(self):
        return [one_tag.id for one_tag in self.tag]
