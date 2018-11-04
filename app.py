from flask import Flask, session, request, redirect, url_for, flash, render_template

import db

app = Flask(__name__)


@app.route('/')
def index():
    if 'user' in session and session['user'] is not None:
        return render_template('index.html', user=session['user'])
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = db.get_user(username, password)
            if user:
                session['user'] = user
            else:
                flash('Username or password is wrong')
        except Exception as e:
            flash(e.message)
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


# really secret secret-key:
app.secret_key = 'NCREDINBURGH'

if __name__ == '__main__':
    app.run(debug=True)
