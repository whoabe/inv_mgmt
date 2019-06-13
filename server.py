import peeweedbevolve
from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, Store
import os

app = Flask(__name__)

app.secret_key = os.getenv('secret_key')

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.cli.command()
def migrate():
    db.evolve(ignore_tables = {'base_model'})

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/store")
def store():
    return render_template('store.html')

@app.route("/store_form", methods = ["POST"])
def create():
    s = Store(name=request.form['name'])
    #s is equal to the class with the name from the html button
    #pulling the informatino from form, not args

    if s.save():
        flash("flash saved")
        return redirect(url_for('store'))
    else:
        return render_template('store.html', name=request.args['name]'])

if __name__ == '__main__':
   app.run()