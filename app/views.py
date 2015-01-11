import re
import hashlib
from app import app, nav, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g, json
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.gravatar import Gravatar
from .forms import LoginForm, SignupForm, PasswordResetForm
from models import User, Task

from werkzeug.security import generate_password_hash

nav.Bar('left_auth', [
    nav.Item('Todo', 'index')
])

nav.Bar('right_auth', [
    nav.Item('Profile', 'profile'),
    nav.Item('Logout', 'logout')
])

nav.Bar('left', [
    
])

nav.Bar('right', [
    nav.Item('Login', 'login')
])

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
  if not g.user.is_authenticated(): 
    return redirect('login')
  if request.method == 'POST':
    data = request.get_json()
    todo = data.get('todo')  # incomplete-tasks
    done = data.get('done')  # complete-tasks

    # Delete all of the user's tasks from the db
    user_tasks = g.user.get_tasks()
    for task in user_tasks:
      tmp_task = task
      db.session.delete(tmp_task)
    db.session.commit()

    # Add the incomplete-tasks to the db
    for task in todo:
      task_body = task
      task_status = 0
      task_user = g.user.get_id() 
      new_task = Task(task_body, task_status, task_user)      
      db.session.add(new_task)
    db.session.commit()

    # Add the complete-tasks to the db
    for task in done:
      task_body = task
      task_status = 1
      task_user = g.user.get_id() 
      new_task = Task(task_body, task_status, task_user)
      db.session.add(new_task)
    db.session.commit()

    return render_template('home.html', todo=todo, done=done)
  if request.method == 'GET':
    user_tasks = g.user.get_tasks()
    todo = [] # incomplete-tasks
    done = [] # complete-tasks
    for task in user_tasks:
      if task.is_complete:
        done.append(task.task)
      else:
        todo.append(task.task)
    return render_template('home.html', title='Home', todo=todo, done=done)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  if request.method == 'POST' and form.validate_on_submit():
    all_good = True
    name = request.form['name']
    email = request.form['email'].lower()
    password = md5(request.form['password'])
    if is_email_valid(email):
      user = User(name, email, password)
      users_all = User.query.all()
      for u in users_all:
        if u.email.lower() == user.email.lower():
          all_good = False
          break
      if all_good == True:
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
      elif all_good == False:
        flash("The email you entered is taken.", 'error')
        return redirect(url_for('signup'))
    else:
      flash("There is something wrong with the data you entered. ", 'error')
      return redirect(url_for('signup'))
  else:
    return render_template('signup.html', title='Signup', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if request.method == 'POST':
    email = request.form['email'].lower()
    password = md5(request.form['password'])
    registered_user = User.query.filter_by(email=email, password=password).first()
    if registered_user is None:
      flash('Username or Password is invalid', 'error')
      return redirect(url_for('login'))
    login_user(registered_user)
    return redirect(request.args.get('next') or url_for('index'))
  return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('login')) 

@app.route('/profile')
def profile():
  name = g.user.name
  email = [g.user.email]
  user = {'name': name, 'email': email}
  gravatar = Gravatar(app,
                    size=200,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)
  return render_template('profile.html', title='Profile', email=email, name=name, gravatar=gravatar)

@app.route('/pw-reset', methods=['POST', 'GET'])
def pw_reset():
  form = PasswordResetForm()
  if request.method == 'POST':
    old_pass = request.form['old_password']
    new_pass = request.form['new_password']
    new_pass_confirm = request.form['new_password_confirm']
    current_pass = g.user.password
    if current_pass == old_pass:
      if new_pass == new_pass_confirm:
        user = User.query.filter_by(name=g.user.name, email=g.user.email, password=old_pass).first()  
        temp_user = user
        db.session.delete(user)
        db.session.commit()
        new_user = User(temp_user.name, temp_user.email, new_pass)
        db.session.add(new_user)
        db.session.commit()
        flash('Password was reset!')
        return redirect(url_for('profile'))
      else:
        flash('Passwords don\'t match. Try again!', 'error')
        return render_template('pw-reset.html', title="Password Reset", form=form)
    else:
      flash('There was an error. Try again!', 'error')
      return render_template('pw-reset.html', title="Password Reset", form=form)
  return render_template('pw-reset.html', title="Password Reset", form=form)

@app.before_request
def before_request():
  g.user = current_user

@lm.user_loader
def load_user(id):
  return User.query.get(int(id))

def is_email_valid(email):
  if re.match(r"[^@]+@[^@]+\.[^@]+", email):
    return True
  else:
    return False

def md5(string):
  return hashlib.md5(string).hexdigest()

