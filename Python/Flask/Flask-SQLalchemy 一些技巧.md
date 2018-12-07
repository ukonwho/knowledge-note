# many to many 表更新

Demo table

```
page_tag_relate=db.Table('page_tag_relate',db.Colum('tag_id',db.Integer,db.ForeignKey('tag.id')),db.Column('page_id',db.Integer,db.ForeignKey('page.id')))

class Page(db.Model):
    __tablename__ = 'page'
    id=db.Column(db.Integer,primary_key=True)
 tags=db.relationship('Tag',secondary=page_tag_relate,backref=db.backref('pages',lazy='dynamic'))

class Tag(db.Model):
    __tablename__ = 'tag'
    db=db.Column(db.Integer,primary_key=True)
```

