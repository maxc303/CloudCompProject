from app import webapp
from datetime import timedelta
from flask import  redirect, url_for, g, session, render_template, request
import app.utils as u
webapp.secret_key = '\x80\xa9s*\x12\xc7x\xa9d\x1f(\x03\xbeHJ:\x9f\xf0!\xb1a\xaa\x0f'
webapp.permanent_session_lifetime = timedelta(days=1)

@webapp.route('/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')



@webapp.route('/', methods=['GET'])
def main():
    new_games = u.list_all_new_games()
    will_release_games = u.list_all_will_release_games()
    free_games = u.list_all_free_games()
    return render_template('main.html', new_games=new_games, will_release_games=will_release_games,free_games=free_games)

@webapp.route('/search', methods=['GET', 'POST'])
def search():
    search_txt = request.form.get('search', "")
    print(search_txt)
    # Return to all if keyword is ""
    if search_txt == "":
        return redirect(url_for('main'))

    #Include search
    #records = u.list_search_results(search_txt)

    #Fuzzy search
    records = u.fuzzy_search(search_txt)

    return render_template('search_result.html', records=records)

