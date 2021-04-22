from flask import render_template, Blueprint, redirect, request, current_app
import datetime as dt
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/index")
def index():
    return render_template("index.html")
