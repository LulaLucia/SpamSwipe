# November 25, 2026 
#Polina P, Meleny S, Lula L
# Modulation for SpamSwipe

import cs304dbi as dbi
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename

def create_post(conn, title, description, exp_date, public, file_name, uid): 
    ''' insert new post information into database '''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''INSERT INTO post
        (title, description, exp_date, public, file_name, uid)
        VALUES (%s, %s, %s, %s, %s, %s)''',
                     [title, description, exp_date, public, file_name, uid]) 
        post_id = curs.lastrowid
    conn.commit()
    return post_id

def get_public_posts(conn):
    """Returns all post that are public"""
    with dbi.dict_cursor(conn) as curs:
        curs.execute(''' select * from post where public = true order by post_id desc''')
        public_posts = curs.fetchall()
    return public_posts

def get_private_posts(conn):
     """Returns all post that are private"""
    with dbi.dict_cursor(conn) as curs:
        curs.execute(''' select * from post where public = false order by post_id desc''')
        private_posts = curs.fetchall()
    return private_posts






