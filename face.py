import peewee

class Face(peewee.Model):
    id = peewee.IntegerField(primary_key = True)
    story = peewee.IntegerField(null = False)
    pic = peewee.IntegerField(null = False)
    x = peewee.IntegerField(null = False)
    y = peewee.IntegerField(null = False)
    w = peewee.IntegerField(null = False)
    h = peewee.IntegerField(null = False)
    chalacter = peewee.TextField()
    path = peewee.TextField()
