from datetime import datetime
import os

from flask import Flask

from flask import request, session, redirect, render_template, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class NameForm(FlaskForm):
    name = StringField('What is your name?')
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/movie')
def movie():
    # Movie Titles - Stored as an array
    movie_names = ['Avatar',
                   'Pirates of the Caribbean',
                   'Spectre',
                   'The Dark Knight Rises',
                   'John Carter',
                   'Spider-Man 3',
                   'Tangled']

    # Movie Titles with Attributes - Stored in a Dictionary
    movies = {
        'Avatar': {'critical_reviews': 723, 'duration': 178, 'imdb_score': 7.9},
        'Pirates of the Caribbean': {'critical_reviews': 302, 'duration': 169, 'imdb_score': 7.1},
        'Spectre': {'critical_reviews': 602, 'duration': 148, 'imdb_score': 6.8},
        'The Dark Knight Rises': {'critical_reviews': 813, 'duration': 164, 'imdb_score': 8.5},
        'John Carter': {'critical_reviews': 462, 'duration': 132, 'imdb_score': 6.6},
        'Spider-Man 3': {'critical_reviews': 392, 'duration': 156, 'imdb_score': 6.2},
        'Tangled': {'critical_reviews': 324, 'duration': 100, 'imdb_score': 7.8},
    }

    return render_template('movie.html', movie_names=movie_names, movies=movies)


@app.route('/status')
def status():
    print('###', status.__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    dt = datetime.now()
    print(dt)
    print('app path:', basedir)
    print('###', status.__name__)
    print(type(dt))
    mytime = dt.strftime("%H시 %M분 %S초")
    print(mytime)
    # return basedir + dt
    # return mytime
    import subprocess
    out = subprocess.check_output('df -h | grep disk', shell=True)
    out = out.decode('ascii')
    return '<pre>' + out + '</pre>'


@app.route('/')
def index():
    # return '<h1>Hello World!</h1>'
    # user_agent = request.headers.get('User-Agent')
    # return '</p>Your browser is %s</p>' % user_agent
    return render_template('index.html', my_list=[x + 1 for x in range(10)], intro_msg='Welcome to Toggi Server',
                           cur_time=datetime.utcnow())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('login'))
    return render_template('login.html', form=form, name=session.get('name'))


@app.route('/user/<name>')
def user(name):
    # return '<h1>Hello %s!</h1>' % username
    return render_template('user.html', name=name)


@app.route('/url')
def url():
    return url_for('static', filename='a.ico', _external=True)


@app.route('/post/<int:post_id>')
def post(post_id):
    return 'Post ID is %s' % post_id


@app.route('/post/<float:post_id>')
def post_float(post_id):
    return 'Post ID is %s (float)' % post_id


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', 500)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, host='0.0.0.0')
    # manager.run()
    # hello(1, 2, 3)

