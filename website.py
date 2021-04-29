from flask import Flask ,render_template,redirect,url_for,request,session

from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)
#app.secret_key = 'super-secret-key'
app.config['SECRET_KEY']='bdhsjdbxjcbhcbhxbcbcc'






#app.config['SQLALCHEMY_DATABASE_URI']="postgresql+psycopg2://postgres:July@2000@localhost/post1"
app.config['SQLALCHEMY_DATABASE_URI']="postgres://woxdzkgbiycmsa:4ac79fe4950e25c6be63b7dd0f47fd3ac9a968160cfc3f26fba9ae8c35cc291e@ec2-54-162-119-125.compute-1.amazonaws.com:5432/d1o2enn4vqfsm2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)


class Favouritepost(db.Model):
 	id=db.Column(db.Integer,primary_key=True)
 	image=db.Column(db.String(1000),nullable=False)
 	heading=db.Column(db.String(1000),nullable=False)
 	paragraph=db.Column(db.String(5000),nullable=False)

class Contact(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(100), nullable=False)
	email=db.Column(db.String(100),nullable=False)
	phone=db.Column(db.String(12),nullable=False)
	message=db.Column(db.String(500),nullable=False)





@app.route('/')
def index():
	result=Favouritepost.query.all()
	return render_template('index.html' ,result=result)

@app.route('/bpadmin',methods=['GET','POST'])
def bpdmin():
	if 'user' in session and session['user']=='Bhuvnesh':
		result=Favouritepost.query.all()
		c=Contact.query.all()
		return render_template('dashboard.html',c=c,result=result)
	if request.method=='POST':
		username=request.form['uname']
		userpassword=request.form['pass']
		if username=='Bhuvnesh' and userpassword=='Golu1998':
			session['user']=username
			result=Favouritepost.query.all()
			c=Contact.query.all()
			return render_template('dashboard.html',c=c,result=result)
	return render_template('login.html')		
	




@app.route('/addpost')
def addpost():
	return render_template('addpost.html')



@app.route('/process',methods=['POST'])
def process():
	image=request.form['image']
	heading=request.form['heading']
	paragraph=request.form['paragraph']
	postdata=Favouritepost(image=image,heading=heading,paragraph=paragraph)
	db.session.add(postdata)
	db.session.commit()
	return redirect(url_for('index'))



@app.route('/edit/<string:id>', methods=['GET','POST'])
def edit(id):
	if 'user' in session and session['user']=='Bhuvnesh':
		#
	    if request.method=='POST':
	        image=request.form['image']
	        heading=request.form['heading']
	        paragraph=request.form['paragraph']
	        p=Favouritepost.query.filter_by(id=id).first()
	        p.image=image
	        p.heading=heading
	        p.paragraph=paragraph
	        db.session.commit()
	        return redirect('/edit/'+ id)
	    p=Favouritepost.query.filter_by(id=id).first()    
	    return render_template('edit.html',p=p,id=id)

@app.route('/delete/<string:id>',methods=['GET','POST'])
def delete(id):
	if 'user' in session and session['user']=='Bhuvnesh':
	    papaya=Favouritepost.query.filter_by(id=id).first()
	    db.session.delete(papaya)
	    db.session.commit()
	    return redirect('/bpadmin')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/processcontact', methods=['POST'])
def processcontact():
	name=request.form['name']
	email=request.form['email']
	phone_num=request.form['phone']
	msg=request.form['message']
	contactdata=Contact(name=name,email=email,phone=phone_num,message=msg)
	db.session.add(contactdata)
	db.session.commit()
	return redirect('/contact')

@app.route('/contactdelete/<string:id>',methods=['GET','POST'])
def contactdelete(id):
	if 'user' in session and session['user']=='Bhuvnesh':
	    deletecontact=Contact.query.filter_by(id=id).first()
	    db.session.delete(deletecontact)
	    db.session.commit()
	    return redirect('/bpadmin')
	
    
@app.route('/logout')
def logout():
	session.pop('user')
	return redirect('/')


@app.route('/view/<string:id>')
def view(id):
	result=Favouritepost.query.filter_by(id=id).first()
	return render_template('view.html',result=result)








if __name__ == '__main__':
	app.run()
	
