from flask import Blueprint, render_template

from . import db


my_view = Blueprint('my_view', __name__)


# Routes to html views with GET requests
@my_view.route("/")
def index():
    return render_template('index.html')

@my_view.route('/viewTables')
def viewTables():
    return render_template('viewtables.html')

@my_view.route('/eventOrder')
def viewEventOrder():
    return render_template('tables/eventorder.html')

@my_view.route('/createDB')
def createdb():
    return render_template('index.html', db.create_all())