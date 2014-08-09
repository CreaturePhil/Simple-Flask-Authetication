from project import app, get_db, query_db
from flask import url_for, render_template, flash, request, session, redirect
from werkzeug import generate_password_hash, check_password_hash

def validate_registration(username, password, confirm):
  username = str(username)
  password = str(password)
  if len(username) == 0 or len(username) > 64 or len(password) <= 6 or len(password) > 52 or password != confirm:
    return False
  return True

def validate_login(username, password, actualname, actualpass):
  if username != actualname or not check_password_hash(actualpass, password):
    return False
  return True

@app.route('/')
def index():
  return render_template('layout.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if session.get('logged_in'):
    return redirect(url_for('index'))

  if request.method == 'POST':
    db = get_db()

    username = request.form['username'].lower()
    password = request.form['password']
    confirm = request.form['confirm']
    if not validate_registration(username, password, confirm):
      flash("Username or password is invalid.")
      return redirect(url_for('register'))

    user = query_db('select * from users where username = ?', [username], one=True)
    if user is not None:
      flash("Username is already taken.")
      return redirect(url_for('register'))

    passhash = generate_password_hash(password)
    db.execute('insert into users (username, password) values (?, ?)', [username, passhash])
    db.commit()
    flash('You have sucessfully register!')
    return redirect(url_for('login'))

  return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if session.get('logged_in'):
    return redirect(url_for('index'))
  if request.method == 'POST':
    username = request.form['username'].lower()
    password = request.form['password']

    user = query_db('select * from users where username = ?', [username], one=True)
    if not validate_login(username, password, user['username'], user['password']):
      flash('Username or password is invalid')
      return redirect(url_for('login'))

    session['logged_in'] = True
    flash('You have succussfully login!')
    return redirect(url_for('index'))

  return render_template('login.html')

@app.route('/logout')
def logout():
  if session.get('logged_in'):
    session.pop('logged_in', None)
    flash('You were logged out')
  return redirect(url_for('login'))

@app.route('/user/<user>')
def profile(user):
  data_user = query_db('select * from users where username = ?', [user], one=True)
  if data_user == None:
    return 'User not found'
  return render_template('profile.html', user = data_user['username'])
