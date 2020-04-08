from app import webapp
from datetime import timedelta
from flask import  redirect, url_for, g, session, render_template, request
import app.utils as u
webapp.secret_key = '\x80\xa9s*\x12\xc7x\xa9d\x1f(\x03\xbeHJ:\x9f\xf0!\xb1a\xaa\x0f'
webapp.permanent_session_lifetime = timedelta(days=1)

@webapp.route('/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')

@webapp.route('/main', methods=['GET'])
def main():
    records = u.list_all()
    return render_template('main.html', records=records)

@webapp.route('/', methods=['GET'])
def list_new_games():
    records = u.list_all_new_games()
    return render_template('cards.html', records=records)

@webapp.route('/search', methods=['GET', 'POST'])
def search():
    search_txt = request.form.get('search', "")
    print(search_txt)
    #Include search
    #records = u.list_search_results(search_txt)
    if search_txt == "":
        records = u.list_all_new_games()
        return render_template('cards.html', records=records)

    #Fuzzy search
    records = u.fuzzy_search(search_txt)
    return render_template('cards.html', records=records)

