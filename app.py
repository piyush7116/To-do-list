from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timezone
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)
class Todo(db.Model):
    sno= db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.now(timezone.utc))
    def __repr__(self):
        return f"{self.sno} - {self.title}"
@app.route("/",methods=['GET','POST'])
def home():
    if request.method=='POST':        
        titles=request.form['title']
        description=request.form['desc']
        todo1=Todo(title=titles ,desc=description)
        db.session.add(todo1)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template('index.html',alltodos=alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    deldata=Todo.query.filter_by(sno=sno).first()
    db.session.delete(deldata)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        titles1=request.form['title']
        description1=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=titles1 
        todo.desc=description1
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

   
if __name__ =="__main__":
    app.run(host='0.0.0.0',debug=True)

 
