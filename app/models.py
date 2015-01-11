from app import db


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password = db.Column(db.String(30), index=True)
  tasks = db.relationship('Task', backref='author', lazy='dynamic')

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    try:
        return unicode(self.id)  # python 2
    except NameError:
        return str(self.id)  # python 3

  def get_tasks(self):
    return Task.query.filter(Task.user_id == self.id).all()


  def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.password = password
    self.tasks = self.get_tasks()

  def __repr__(self):
    return '<User %r' % (self.name)

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  task = db.Column(db.String(40))
  is_complete = db.Column(db.Boolean)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __init__(self, task, is_complete, user_id):
    self.task = task
    self.is_complete = is_complete
    self.user_id = user_id

  def __repr__(self):
    return '<Task %r>' % (self.task)

