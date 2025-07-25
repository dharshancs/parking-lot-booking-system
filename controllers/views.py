from flask import Blueprint, render_template    

view = Blueprint("base",__name__)

@view.route('/')
def index():
    return render_template('index.html')