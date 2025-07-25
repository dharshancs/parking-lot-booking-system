from flask import Blueprint, render_template, flash, request


b_view = Blueprint("base",__name__)   

@b_view.route('/')
def index():
    return render_template('index.html')



