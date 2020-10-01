from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Item

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@bp.route('/search')
def search():
    if request.args['search']:
        ite = "%" + request.args['search'] + "%"
        items = Item.query.filter(Item.name.like(ite)).all()
        return render_template('index.html', items=items)
    else:
        return redirect(url_for('main.index'))