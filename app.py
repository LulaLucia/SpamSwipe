## Polina, Meleny, Lula
# Flask root application to define flask instance and define routes

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

import secrets
import cs304dbi as dbi

# we need a secret_key to use flash() and sessions
app.secret_key = secrets.token_hex()

# configure DBI
dsn = dbi.conf('mlp_db')

# For Lookup, use 'wmdb'
# For CRUD and Ajax, use your personal db
# For project work, use your team db

print(dbi.conf('mlp_db'))

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    return render_template('main.html', page_title='Main Page')

@app.route('/about/')
def about():
    flash('this is a flashed message')
    return render_template('about.html', page_title='About Us')

#
@app.route('/profile/')
def profile():
    return render_template('profile.html', page_title='Profile')

#
@app.route('/login/')
def login():
    return render_template('login.html', page_title='Login')

#
@app.route('/post/', methods = ['POST'])
def create_post():
    return render_template('create_post.html', page_title='Create a Post')
                        

#
@app.route('/saved/')
def saved_posts():
    return render_template('saved_posts.html', page_title='Saved Posts')

#
@app.route('/following/')
def following_feed():
    return render_template('following_feed.html', page_title='Following Feed')



if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
