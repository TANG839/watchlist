import os
import click
from flask import Flask
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy # import SQLAlchemy 扩展类



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')      # 设置数据库 URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db= SQLAlchemy(app)  # 初始化扩展，传入程序实例 app


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop: 
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


@app.cli.command()                   #create a command forge to generate fake data
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'Fuyao Tang'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)  # create a new user 
    db.session.add(user)    # add the user to the database
    for m in movies:        # m is each dictionary
        movie = Movie(title=m['title'], year=m['year'])    # create each movie
        db.session.add(movie) # add each movie to the database

    db.session.commit()
    click.echo('Done.')  # output information


class User(db.Model): # table name will be user, model class inherits from db.Model
    id = db.Column(db.Integer, primary_key=True)  # primary key
    name = db.Column(db.String(20))  # name
class Movie(db.Model):  # table name will be movie
    id = db.Column(db.Integer, primary_key=True)  # primary key
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.context_processor      # register a context processor function
def inject_user():
    user = User.query.first()
    return dict(user=user)        # return a dictionary, equal to {'user': user}


@app.errorhandler(404)          # register an error handler
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index(): #define a view function 索引（首页）
    # user = User.query.first() # get the first user
    movies = Movie.query.all() # get all movies
    return render_template('index.html', movies=movies) #pass the value of user and movies to the template