import os, time, datetime, json
from app import app, db
from flask import render_template, request, redirect, url_for, jsonify, g, session, flash
from flask.ext.wtf import Form 
from wtforms.fields import TextField, FileField, SelectField # other fields include PasswordField 
from wtforms.validators import Required
from app.models import Myprofile
from app.forms import LoginForm
from werkzeug.utils import secure_filename
import random


SECRET_KEY="super secure key"
app.config.from_object(__name__)


class ProfileForm(Form):
    image = FileField(u'Image File',  validators=[Required()])
    firstname = TextField('First Name', validators = [Required()])
    lastname = TextField('Last Name', validators = [Required()])
    age = TextField('Age', validators = [Required()])
    sex = SelectField(u'Sex', choices = [('Male', 'Male'), ('Female', 'Female')])


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
    

@app.route('/login/', methods=['POST','GET'])
def login():
    form = LoginForm(request.form)
    error = None
    try:
        if request.method == 'POST':
            attempted_username = request.form['username']
            db_username = Myprofile.query.filter(Myprofile.username == attempted_username).one()
            attempted_password = request.form['password']
            
            if attempted_username == db_username.username and attempted_password == "password":
                return redirect(url_for('profile_list'))
            else:
                error = 'Invalid credentials'
        return render_template("login.html",error=error,form=form)
    except Exception as e:
        flash(e)
        return render_template("login.html",error=error,form=form)


@app.route('/profile/', methods = ['POST','GET'])
def newprofile():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        sex = request.form['sex']
        age = request.form['age']
        form = ProfileForm(request.form)
        image = request.files['image']
        UPLOAD_FOLDER = "/app/static/uploads"
        imagename = secure_filename(image.filename)
        
        image.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, imagename))
        username = firstname[:1] + lastname + age + time.strftime("%Y")
        check = db.session.execute('SELECT max(id) from myprofile')
        if check is True:
            for i in check:
                userid = i[0] + 1
        else:
            userid = 6200
        return "Hello"
        newProfile = Myprofile(id=userid,firstname=firstname, lastname=lastname, sex=sex, age=age, username=username, image=imagename)
        db.session.add(newProfile)
        db.session.commit()
        flash('New entry was successfully posted')
        return redirect('/profile/'+str(Myprofile.query.filter_by(username=newProfile.username).first().id))
    form = ProfileForm()
    return render_template('registration.html',form=form)


@app.route('/profiles/',methods=["POST","GET"])
def profile_list():
    profiles = db.session.query(Myprofile).all()
    if request.method == "POST":
        profilelisting=[]
        for profiles in profiles:
            profilelisting.append({'id':profiles.id,'username':profiles.username})
        return jsonify(profiles=profilelisting)
    else:
        return render_template('profile_list.html',profiles=profiles)


@app.route('/profile/<userid>')
def profile_view(userid):
    timeinfo = time.strftime("%a, %b %d %Y")
    profile = Myprofile.query.filter_by(id=userid).first()
    image = url_for('static', filename='uploads/'+profile.image)
    if request.method == 'POST':
        return jsonify(id=profile.id,username=profile.username,image=image,sex=profile.sex, age=profile.age)
    else:
        profile_vars = {'id':profile.id, 'username':profile.username, 'image':image, 'age':profile.age, 'firstname':profile.firstname, 'lastname':profile.lastname, 'sex':profile.sex}
    return render_template('profile_view.html',profile=profile_vars,curr_date=timeinfo)


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
