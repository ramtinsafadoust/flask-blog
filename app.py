from flask import Flask,redirect,request,flash,session,url_for,g,jsonify,json,render_template
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
import secrets
import jdatetime
from werkzeug.utils import secure_filename


app = Flask(__name__)
secret = secrets.token_urlsafe(32)
app.secret_key = secret
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)
Login_manager= LoginManager()
Login_manager.init_app(app)
jdatetime.set_locale('fa_IR')



class posts(db.Model):

    id= db.Column("id", db.Integer , primary_key=True)
    tittle=db.Column(db.String(200))
    content=db.Column(db.Text)
    writer=db.Column(db.String(100))
    date=db.Column(db.String(100))
    img=db.Column(db.Text)
    imgname=db.Column(db.Text)
    mimetype=db.Column(db.Text)

class users(UserMixin,db.Model):
    id=db.Column("id",db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(100))
    surename=db.Column(db.String(100))
    level=db.Column(db.Integer)


    def __repr__(self):
        return f"devices('{self.username}','{self.password}','{self.surename}','{self.level}')"

@Login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

    
@app.route('/',methods=["POST","GET"])
def index():

    return render_template("index.html",values=posts.query.all())

@app.route('/addpost',methods=["POST","GET"])
def addpost():
    if request.method=="POST":
        date=jdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
        writer="Ramtin Safadoust"
        tittle=request.form["tittle"]
        content=request.form["content"]
        picture=request.files["picture"]
        filename=secure_filename(picture.filename)
        mimetype=picture.mimetype


        newpost=posts(tittle=tittle,content=content,writer=writer,date=date,img=picture.read(),imgname=filename,mimetype=mimetype)
        
       



        db.session.add(newpost)
        db.session.commit()
        return "OK"
    return render_template("addpost.html")



if __name__ == '__main__':
    
    app.run(debug=True)
    