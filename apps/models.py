from exts import db
from datetime import datetime
class BannersModel(db.Model):
    __tablename__="banners"
    id=db.Column(db.Integer ,primary_key=True,autoincrement=True)
    name=db.Column(db.String(255),nullable=False)
    image_url=db.Column(db.String(255),nullable=False)
    link_url=db.Column(db.String(255),nullable=False)
    priority=db.Column(db.Integer,default=0)
    create_time=db.Column(db.DateTime,default=datetime.now)

class BoardsModel(db.Model):
    __tablename__="boards"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(25),nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)


#发布帖子表单  与板块表单建立外键,与用户表建立外键关系，表明帖子属于哪个板块那个作者
class Aposts(db.Model):
    __tablename__="post"
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    title=db.Column(db.String(200), nullable=False)
    content=db.Column(db.Text, nullable=False)
    image_src=db.Column(db.String(200))
    create_time=db.Column(db.DateTime,default=datetime.now)
    board_id=db.Column(db.Integer,db.ForeignKey("boards.id"))
    author_id=db.Column(db.String(100),db.ForeignKey("front_user.id"),nullable=False)


    board=db.relationship("BoardsModel",backref="posts")
    author=db.relationship("FrontUser",backref="posts")



#帖子加精
class HighlightModel(db.Model):
    __tablename__="high_light"
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    post_id=db.Column(db.Integer,db.ForeignKey("post.id"))
    create_time=db.Column(db.DateTime,default=datetime.now)

    post=db.relationship("Aposts",backref="highlight")



#评论模型
class CommentModel(db.Model):
    __tablename__="comment"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.Text,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)
    post_id=db.Column(db.Integer,db.ForeignKey("post.id"))
    author_id=db.Column(db.String(100) ,db.ForeignKey("front_user.id"), nullable=False)

    post=db.relationship("Aposts",backref="comments")
    author=db.relationship("FrontUser",backref="comments")