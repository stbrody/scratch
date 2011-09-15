from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import pymongo

app = Flask(__name__)
app.config.from_object('config')

db = pymongo.Connection(host = app.config['MONGO_URL'],
                        port = int(app.config['MONGO_PORT'])).blog

@app.route('/')
def main():
    return render_template('entries.html')

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
            return redirect(url_for('entries'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run()
