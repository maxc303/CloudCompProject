from app import webapp
from datetime import timedelta
from flask import  redirect, url_for, g, session, render_template, request
import app.utils as u
webapp.secret_key = '\x80\xa9s*\x12\xc7x\xa9d\x1f(\x03\xbeHJ:\x9f\xf0!\xb1a\xaa\x0f'
webapp.permanent_session_lifetime = timedelta(days=1)

@webapp.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')

@webapp.route('/main', methods=['GET'])
def main():
    records = u.list_all()
    return render_template('main.html', records=records)

@webapp.route('/new_games', methods=['GET'])
def list_new_games():
    records = u.list_all_new_games()
    return render_template('cards.html', records=records)


@webapp.route('/search', methods=['GET', 'POST'])
def search():
    search = request.form.get('search', "")
    return search

