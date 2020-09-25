from flask import Blueprint, render_template, request, session, redirect, url_for

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('Items/create.html')
