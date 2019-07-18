from flask import render_template

from user import user


@user.route('/login')
def login():
    return render_template('login.html')