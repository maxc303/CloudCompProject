from app import webapp
from datetime import timedelta
from flask import template_rendered, redirect, url_for, g, session

webapp.permanent_session_lifetime = timedelta(days=1)

@webapp.route('/', methods=['GET', 'POST'])
def main():
    return 'hello world'
