import requests
from flask import Blueprint, render_template, redirect, url_for
from settings import settings


ui = Blueprint('ui', __name__)


@ui.route('/')
def root():
    return redirect(url_for('ui.home'))


@ui.route('/short-url/home')
def home():
    resp = requests.get(f'{settings.API_ENDPOINT}/v1/url')

    return render_template('home.html', urls=resp.json()['urls'])


@ui.route('/<string:short_url>')
def redirect_origin_url(short_url):
    resp = requests.get(f'{settings.API_ENDPOINT}/v1/url/{short_url}')

    if not resp.ok:
        return f'<a href="/short-url/home">{resp.json().get("message", "Error")}<a>'

    return redirect(resp.json()['origin_url'])
