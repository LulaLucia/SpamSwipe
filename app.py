import os
# Polina, Meleny, Lula
# Flask root application to define flask instance and define routes

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename

app = Flask(__name__)

from passlib.context import CryptContext
from datetime import datetime, timedelta
from pymysql import IntegrityError

import secrets
import cs304dbi as dbi
import query

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    default="argon2",
    deprecated=["bcrypt"],

    bcrypt__rounds=12,
    bcrypt__ident="2b",
    bcrypt__truncate_error=True,

    argon2__memory_cost=65536,  # 64 MB
    argon2__time_cost=3,
    argon2__parallelism=4,
)


#was causing a new key to be created every time page refreshed even if same user/session
# we need a secret_key to use flash() and sessions
#app.secret_key = secrets.token_hex()
app.secret_key = 'secretekey'

# configure DBI
dsn = dbi.conf('mlpteam_db')

# For Lookup, use 'wmdb'
# For CRUD and Ajax, use your personal db
# For project work, use your team db

print(dbi.conf('mlpteam_db'))

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

# new for file upload
app.config['UPLOADS'] = '/students/mlpteam/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 1*1024*1024 # 1 MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

@app.route('/')
def index():
    if session.get('logged_in'):
        conn = dbi.connect()
        curs = dbi.dict_cursor(conn)
        curs.execute('''select post_id, title, description, exp_date, file_name from post''')
        post = curs.fetchall()
        return render_template('main.html', page_title='Home', username=session.get('username'), post = post)
    else: 
        return redirect(url_for('login_page'))

@app.route('/about/')
def about():
    return render_template('about.html', page_title='About Us')

#
@app.route('/profile/')
def profile(): 
    #checks if logged in
    if not session.get('logged_in'):
       flash("Please log in first")
       return redirect(url_for('index'))

    uid = session.get('uid')
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    
    #user info
    curs.execute('''select username, name, org_acct, email from user where uid = %s''', [uid])
    user = curs.fetchone()

    #posts
    curs.execute('''select post_id, title, description, exp_date, file_name from post where uid = %s''', [uid])
    post = curs.fetchall()

    return render_template('profile.html', page_title='Profile', user = user, post = post)

#
@app.route('/signup/', methods = ["POST"])
def signup():
    username = request.form.get("username").strip()
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    name = request.form.get("name").strip()
    email = request.form.get("email").strip()
    org = request.form.get("org")

    if username == '':
        flash('username is required')
        print("redirecting 2 from signup")
        return redirect(url_for('login_page'))
    if password1 == '':
        flash('password is required')
        print("redirecting 3 from signup")
        return redirect(url_for('login_page'))
    if email == '' or ("@wellesley.edu" not in email):
        flash('student email is required')
        print("redirecting 4 from signup")
        return redirect(url_for('login_page'))
    if name == '':
        flash('name is required')
        print("redirecting 5 from signup")
        return redirect(url_for('login_page'))
    if password1 != password2:
        flash("passwords do not match")
        print("redirecting 6 from signup")
        return redirect(url_for("login_page"))
    
    hashed = pwd_context.hash(password1)
    print(hashed)

    with dbi.connect() as conn:
        with dbi.cursor(conn) as curs:
            try:
                curs.execute('''INSERT INTO user(uid, username, name, password, email, org_acct) VALUES(NULL, %s, %s, %s, %s, %s)''', [username, name, hashed, email, org])
                conn.commit()
                uid = curs.lastrowid
            except IntegrityError as err:
                flash('That username is taken: {}'.format(repr(err)))
                print("redirecting 7 from signup dbi")
                return redirect(url_for('login_page'))
            
            session['username'] = username
            session['uid'] = uid
            session['logged_in'] = True

            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('logged_in', "True", expires = datetime.now()+timedelta(days=30))
            return resp

@app.route('/login/', methods = ["POST"])
def login():
    username = request.form.get("username").strip()
    password = request.form.get("password")

    if not username or not password:
        flash('Username and password are required.')
        print("redirecting 8 from login")
        return redirect(url_for('login_page'))
    
    with dbi.connect() as conn:
        with dbi.cursor(conn) as curs:
            curs.execute('''SELECT uid, password FROM user WHERE username = %s''', [username])
            row = curs.fetchone()
                
            if row is None:
                flash('Login incorrect. Try again or sign up.')
                return redirect(url_for('index'))
            stored = row[1]
            okay, newhash = pwd_context.verify_and_update(password, stored)

            if okay:
                print("They matched!")
                flash("Successfuly logged in as " +username)
                session['username'] = username
                session['uid'] = row[0]
                session['logged_in'] = True
                print("session after: ", session)
                return redirect(url_for('index'))
                if newhash is not None:
                    curs.execute('''update user set password = %s where uid = %s''', [newhash, row['uid']])
                    conn.commit()
                resp = make_response(redirect(url_for('index')))
                resp.set_cookie('logged_in', "True", expires=datetime.now() + timedelta(days=30))
                return resp
            else:
                flash("Login incorrect. Try again or register")
                print("redirecting 9 from login")
                return redirect(url_for('login_page'))

@app.route('/login_page/')
def login_page():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('login.html', page_title='Welcome / Log In')

@app.route('/logout/')
def logout():
    session.clear()
    print("redirecting 10 from logout")
    resp = make_response(redirect(url_for('login_page')))
    resp.set_cookie('logged_in', '', expires=0)
    flash('Logged out successfully.')
    return resp

#
@app.route('/post/', methods = ['GET', 'POST'])
def create_post():
    '''uploads create_post form information into database
        and processes files'''
    if request.method == 'POST': 
         title = request.form.get('title')
         description = request.form.get('description')
         #tag = request.form.get('tag')
         exp_date = request.form.get('exp_date')
         public = request.form.get('visibility') == 'public'

         uid = session.get('uid')
         if uid is None:
             return redirect(url_for('login'))

         # get uploaded file
         f = request.files.get('file_name')

         if f is None or f.filename == '':
             flash('Please select a file.')
             return redirect(url_for('create_post'))

         original_name = secure_filename(f.filename)
         extension = original_name.rsplit('.', 1)[-1].lower()

         if '.' not in original_name or extension not in ALLOWED_EXTENSIONS:
             flash('Inavlid file type.')
             return redirect(url_for('create_post'))

        # name file
         file_name = secure_filename(f.filename)


        # save file
         pathname = os.path.join(app.config['UPLOADS'], file_name)
         f.save(pathname)
         os.chmod(pathname, 0o444)

        # add post to db
         with dbi.connect() as conn:
              post_id = query.create_post(conn, title, 
                                          description, exp_date,
                                          public, file_name, uid) 
              flash('Post uploaded successfully.')
              return redirect(url_for('profile'))
         
    return render_template('create_post.html', page_title = 'Create a Post')
     
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(
        app.config['UPLOADS'], filename
    )

@app.route('/edit/<int:post_id>', methods = ['GET', 'POST'])
def edit_post(post_id):
    if not session.get('logged_in'):
        flash('Please log in first.')
        return redirect(url_for('index'))

    uid = session.get('uid')

    with dbi.connect() as conn:
        with dbi.dict_cursor(conn) as curs:

            curs.execute('''select * from post 
                            where post_id = %s and uid = %s''',
                         [post_id, uid])

            post = curs.fetchone()

            if post is None:
                flash('Post not found.')
                return redirect(url_for('profile.html'))

            if request.method == 'POST':
                title = request.form.get('title')
                description = request.form.get('description')
                #tag = request.form.get('tag')
                exp_date = request.form.get('exp_date')
                public = request.form.get('visibility') == 'public'

                curs.execute('''update post
                set title = %s, description = %s, 
                exp_date = %s, public = %s
                where post_id = %s and uid = %s''', [title, description, exp_date,
                                                     public, post_id, uid]
                                                    )
                conn.commit()

                flash('Post updated successfully!')
                return redirect(url_for('profile'))

    return render_template('edit_post.html', page_title='Edit Post', post=post)





#page showing all saved post for the logged in user
@app.route('/saved/', methods = ['GET'])
def saved_posts():
    #checks if logged in
    if not session.get('logged_in'):
        flash("Please log in first")
        return redirect(url_for('index'))
    
    uid = session.get('uid')
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
        
    #user info
    curs.execute('''select username, name, org_acct, email from user where uid = %s''', [uid])
    user = curs.fetchone()
    
    #posts
    curs.execute('''select title, description, exp_date, file_name from post 
                    inner join saved 
                    on post.post_id = saved.post_id
                    where saved.uid = %s''', [uid])
    savedpost = curs.fetchall()
    
    return render_template('saved_posts.html', page_title='Saved Posts', user = user, savedpost = savedpost)

@app.route('/savepost/', methods = ['POST'])
def savepost():
    uid = session.get('uid')
    postid = request.form.get('post_id')
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    #stops from user saving post twice, prob wont be needed in final version
    curs.execute('''select * from saved where uid = %s and post_id = %s''', [uid, postid])
    dup = curs.fetchone()
    if dup:
        flash('Already Saved')
    else: 
        curs.execute('''insert into saved(uid,post_id) values (%s, %s)''',[uid, postid])
        conn.commit()
        flash('Saved!')
        return redirect(url_for('index'))
    return redirect(url_for('index'))


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
