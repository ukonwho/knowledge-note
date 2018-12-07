# many to many 表更新

## Demo table

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

## 两张表同时插入新对象
如果场景需要插入Page的同时，也插入tag 
做法是新创建888的对象

```
page_ins_info_dict = {"id": '333'}
page = Page(**page_ins_info)
tag = Tag(id='888') #表中并没有888，是新插入
page.tags.append(tag)
db.session.add(page)
db.session.commit()
```

## 单张表插入新对象，另外一张使用原来的数据
如果是场景tag里面已经有888，只需要新插入一个page，并关联到888 
做法是将888的对象查找到，并传进到关联表对象里面

```
page_ins_info_dict = {"id": '333'}
page = Page(**page_ins_info)
tag = db.session.query(Tag).filter(Tag.id=='888').all()
page.tags = tag
db.session.add(page)
db.session.commit()
```


