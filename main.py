import flask
import flask_login

import config
import models

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'photography'

app.jinja_env.globals['config'] = config

login_manager = flask_login.LoginManager(app)

library = models.Library(config.storage['albums'])

models.Album.to_url = lambda a: flask.url_for('album', album_name=a)
models.Photo.to_url = lambda p: flask.url_for('photo', album_name=p.album, filename=p)
models.Thumbnail.to_url = lambda t: flask.url_for('thumbnail', album_name=t.photo.album, filename=t.photo)


@login_manager.user_loader
def load_user(user_id):
    return models.User.get(user_id)


@app.route('/')
def index():
    return flask.render_template('index.html', albums=library.albums)


@app.route('/album/<album_name>', methods=['GET', 'POST'])
def album(album_name: str):
    _album = library[album_name]
    if flask.request.method == 'POST':
        val = flask.request.form.get('public')
        if val is not None:
            _album.public = (val == 'True')
        return flask.redirect(flask.request.path)
    return flask.render_template('album.html', album=library[album_name])


@app.route('/photo/<album_name>/<filename>')
def photo(album_name: str, filename: str):
    return flask.send_file(library[album_name][filename].path)


@app.route('/thumbnail/<album_name>/<filename>')
def thumbnail(album_name: str, filename: str):
    return flask.send_file(library[album_name][filename].thumbnail.path)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')
        remember = True if flask.request.form.get('remember') else False

        user = models.User.get_by_login_and_password(username, password)
        if not user:
            flask.flash('Please check your login details and try again.')
            return flask.redirect(flask.url_for('login'))

        # flask.flash('Logged in successfully.')
        flask_login.login_user(user, remember=remember)

        return flask.redirect(flask.url_for('index'))
    return flask.render_template('login.html')


@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))
