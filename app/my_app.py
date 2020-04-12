from flask import Flask

from datetime import timedelta
from flask import  redirect, url_for, g, session, render_template, request
import app.utils as u
import os, boto3
from app.config import ALLOWED_EXTENSIONS,UPLOAD_FOLDER

webapp = Flask(__name__)

webapp.secret_key = '\x80\xa9s*\x12\xc7x\xa9d\x1f(\x03\xbeHJ:\x9f\xf0!\xb1a\xaa\x0f'
webapp.permanent_session_lifetime = timedelta(days=1)

def allowed_file(filename):
    """
    :param filename: input file name
    :return: allowed extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    file = request.files['file']
    if file.filename != '':
        if file and allowed_file(file.filename):
            filename = file.filename
            s3 = boto3.client('s3')
            key = 'upload/' + filename
            s3.upload_fileobj(file, 'ps4img', key)
            response = u.text_detect(key)
            records = u.image_text_search(response)
            if not records:
                records = u.search_genre(key)
            return render_template('search_result.html', records=records)
    else:
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


if __name__ == '__main__':
 webapp.run()
