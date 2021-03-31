import os
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import sqlite3

def get_db_connection():
  conn = sqlite3.connect('database.db')
  conn.row_factory = sqlite3.Row
  return conn

def get_post(post_id):
  conn = get_db_connection()
  post = conn.execute('SELECT * FROM posts WHERE id = ?',(post_id,)).fetchone()
  conn.close()
  if post == None:
    abort(404)
  return post

app = Flask(__name__)
# a secret :O

# secret is made secre agan :D
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

@app.route('/')
def index():
  conn = get_db_connection()
  posts = conn.execute('SELECT * FROM posts').fetchall()
  conn.close()
  return render_template('index.html',posts=list(reversed(posts)))

@app.route('/<int:post_id>')
def post(post_id):
  post = get_post(post_id)
  return render_template('post.html', post=post)

@app.route('/create',methods=('GET','POST'))
def create():
  if request.method == "POST":
      title = request.form['title']
      content = request.form['content'] 

      if not title:
        flash('Title is required!')#haha idiot lol # haha
      else:
        conn = get_db_connection()
        conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
  return render_template('create.html')

@app.route('/<int:id>/edit',methods=("GET",'POST'))
def edit(id):
  post = get_post(id)

  if request.method == 'POST':
    title = request.form['title']
    content = request.form['content']

    if not title:
      flash('Title is required!')
    else:
      conn = get_db_connection()
      conn.execute('UPDATE posts SET title = ?, content = ?'' WHERE id = ?',(title, content, id))
      conn.commit()
      conn.close()
  return render_template('edit.html',post=post)

# fixed it issue - ch1ck3n
@app.route('/<int:id>/delete', methods=['POST'])
def delete(id):
  post = get_post(id)
  conn = get_db_connection()
  conn.execute('DELETE FROM posts WHERE id = (?)', (id))
  conn.commit()
  conn.close()
  flash('"{}" was successfully deleted!'.format(post['title']))
  return redirect(url_for('index'))

app.run(host = '0.0.0.0', port = 8080)
#import time, sys
#def sp(text):
#  for char in text:
#    print(char, end = "")
#    time.sleep(0.05)
#    sys.stdout.flush()
# I think
# that
# I'm an idiot
# And I will always be one
# hmmm
# Yep, looks right