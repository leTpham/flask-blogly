"""Blogly application."""

from flask import Flask, render_template, redirect, flash, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

db.create_all()

# SKELETON

@app.get('/')
def homepage():
    return redirect('/users')

@app.get('/users')
def show_users():
    ## each name is a link to route for show_user based on the target's primary key
    all_users = User.query.all()
    
    return render_template('user_listing.html', all_users = all_users)

@app.get('/users/new')
def show_add_user_form():
    return render_template('new_user_form.html')

@app.post('/users/new')
def add_user():
    #get form data
    form_data = request.form
    first_name = form_data["first_name"]
    last_name = form_data["last_name"]
    image_url = form_data["image_url"]
    
    #instantiate new user
    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    
    #send user information to database and update
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user(user_id):
    #need to access user_id
    first_name = User.query.get(user_id).first_name
    last_name = User.query.get(user_id).last_name
    image_url = User.query.get(user_id).image_url
    return render_template('user_detail.html', user_id = user_id,
    first_name = first_name, last_name = last_name, image_url = image_url)

@app.get('/users/<int:user_id>/edit')
def show_edit_user_page(user_id):
    return render_template('user_edit.html', user_id=user_id)


@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    #use the user id to update DB information?

    form_data = request.form
    
    User.query.get(user_id).first_name = form_data["first_name"]
    User.query.get(user_id).last_name = form_data["last_name"]
    User.query.get(user_id).image_url = form_data["image_url"]
    
    db.session.commit()
    
    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    #use user id to delete DB information?
    #flash message user deleted?
    
    User.query.filter(User.id == user_id).delete()
    
    db.session.commit()
    
    return redirect('/users')
