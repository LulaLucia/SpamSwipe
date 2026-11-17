# Lula, Polina, Meleny
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





