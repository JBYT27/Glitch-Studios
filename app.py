import os
from flask import Flask, render_template, request, url_for, flash, redirect, send_from_directory
from werkzeug.exceptions import abort
import sqlite3
import markdown2
import requests

os.system("clear")  # to clear the console a bit
isDark = False
# name = os.environ['REPL_OWNER']
# if (name == "darkdarcool"): username="darkdarcool" yeeted out of existence haha --oh noes mario!

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id, )).fetchone()
    conn.close()
    if post == None:
        abort(404)
    return post


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
# a secret :O

# secret is made secre agan :D
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route('/')
def index():
    print("Main page")
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template(
        'index.html',
        #name = request.headers['X-Replit-User-Name'],
        username = request.headers['X-Replit-User-Name'],
        posts=list(reversed(posts)),
    )


@app.route('/login')
def login():
    print("Logging in!")
    return render_template(
        'login.html',
        name = "bababooey",
        user_id=request.headers['X-Replit-User-Id'],
        username=request.headers['X-Replit-User-Name'],
    )  

@app.route('/logout')
def logout():
  print("oofers, logging out :((")
  return render_template(
    'logout.html',
  )


@app.route('/creators')
def creators():
  print("oooooooh, someone wants to know this!!")
  return render_template(
    'creators.html'
  )

@app.after_request
def remove_header(response):
  #del(response.headers('X-Replit-User-Name'))
  #del username, user_id
  
  return response

@app.route('/<int:post_id>')
def post(post_id):
    print("someone's visiting a post!")
    post = get_post(post_id)
    return render_template('post.html',
                           post=post,
                           content=markdown2.markdown(post["content"]),
                           username=request.headers['X-Replit-User-Name'])


@app.route('/create', methods=('GET', 'POST'))
def create():
    print("someone's creating a post!")
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')  #haha idiot lol # haha
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                         (title,content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=("GET", 'POST'))
def edit(id):
    print("someone's editing a post!")
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute(
                'UPDATE posts SET title = ?, content = ?'
                ' WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
    return render_template('edit.html', post=post)


# fixed it issue - ch1ck3n
@app.route('/<int:id>/delete', methods=('POST', ))
def delete(id):
    print("sad, someone's deleting a post :((")
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id, ))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


@app.route('/favicon.jpg')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'dynamic'),
    'favicon.jpg',
    mimetype='image/vnd.microsoft.icon')


app.run(host='0.0.0.0', port=8080)