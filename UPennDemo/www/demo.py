from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import pymongo
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')

db = pymongo.Connection(host = app.config['MONGO_URL'],
                        port = int(app.config['MONGO_PORT'])).blog

def getPosts(user='admin',num=10):
    return db.posts.find({'username':user}).limit(10).sort('timestamp',pymongo.DESCENDING)

@app.route('/')
def home():
    posts = getPosts()
    return render_template('posts.html', posts=posts)

@app.route('/add', methods=['POST'])
def add_post():
    if not session.get('logged_in'):
        abort(401)
    post = {'username':'admin',#request.form['username'],
            'title':request.form['title'],
            'body':request.form['body'],
            'timestamp':datetime.utcnow()}
    db.posts.insert(post)
    flash('New post was created successfully')
    return redirect(url_for('home'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
