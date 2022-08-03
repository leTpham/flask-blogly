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
    ##links to view detail page
    ##feed data to populate user list
    ##link to add user form
    ## each name is a link to route for show_user based on the target's primary key
    all_users = User.query.all()

    return render_template('user_listing.html', all_users = all_users)

@app.get('/users/new')
def show_add_user_form():
    return render_template('new_user_form.html')

@app.post('/users/new')
def add_user():
    #process add form, add new user
    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user(user_id):
    #need to access user_id
    first_name = User.query.get(user_id).first_name
    last_name = User.query.get(user_id).last_name
    image_url = User.query.get(user_id).image_url
    return render_template('user_detail.html', user_id = user_id,
    first_name = first_name, last_name = last_name, image_url = image_url)

@app.get('/user/<int:user_id>/edit')
def show_edit_user_page():

    return render_template('user_edit.html')

@app.post('/user/<int:user_id>/edit')
def edit_user():
    #use the user id to update DB information?

    return redirect('/users')

@app.post('/user/<int:user_id>/delete')
def delete_user():
    #use user id to delete DB information?
    #flash message user deleted?
    return redirect('/users')
