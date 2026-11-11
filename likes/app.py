from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

import cs304dbi as dbi
import secrets

app.secret_key = secrets.token_hex() # good dynamic key

# table of items and a like count for each

likes_table = {
    'apple': 7,
    'banana': 8,
    'coconut': 0,
    'date': 2}

@app.route('/')
def index():
    return render_template('main.html', items = likes_table.items())

@app.route('/likes/')
def all_likes():
    return jsonify(likes_table)

# Create a new item, count pair. Same endpoint as above, but different METHODS

@app.route('/likes/', methods=['POST'])
def new_item():
    print('request.form', request.form)
    item = request.form.get('item')
    count = request.form.get('count')
    likes_table[item] = int(count)
    print('table', likes_table[item])
    return jsonify({'error': False, 'likes': likes_table[item]})
    
# Handles all methods for this endpoint in a single function.

@app.route('/likes/<item>', methods=['GET','POST','PUT','DELETE'])
def item_likes(item):
    print('method', request.method)
    print('item', item)
    if item not in likes_table:
        return jsonify({'error': 'no such item'})
    if request.method == 'GET':
        print('likes', likes_table[item])
        return jsonify({'error': False, 'likes': likes_table[item]})
    elif request.method == 'POST':
        likes_table[item] += 1
        print('likes', likes_table[item])
        return jsonify({'error': False, 'likes': likes_table[item]})
    elif request.method == 'PUT':
        print('PUT form', request.form)
        likes_table[item] = int(request.form.get('set_likes'))
        print('likes', likes_table[item])
        return jsonify({'error': False, 'likes': likes_table[item]})
    elif request.method == 'DELETE':
        likes_table.pop(item)
        return jsonify({'error': False})
    else:
        return jsonify({'error': 'method not supported'})

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
