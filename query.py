# Lula, Polina, Meleny
# Modulation for SpamSwipe

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
import cs304dbi as dbi


def create_post(conn):
    ''' insert new post information into database '''
    with dbi.dict_cursor(conn) as curs:
        title = request.form.get('post_title')
        description = request.form.get('description')
        tag = request.form.get('tag')
        expiry_date = request.form.get('expiry_date')
        visibility = request.form.get('visibility')
        pic = request.form.get('pic')
        uid = request.form.get('uid')
        curs.execute('''INSERT INTO post (title, description, tag, expiry_date, visibility, pic, uid) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                     (title, description, tag, expiry_date, visibility, pic, uid))
    conn.commit()

