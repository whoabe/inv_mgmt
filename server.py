import peeweedbevolve
from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, Store, Warehouse
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



@app.route("/warehouse")
def warehouse():
    stores  = Store.select() #passing stores from the database into the site
    return render_template('warehouse.html', stores=stores)
    #render_template renders warehouse.html and sets the stores variable to stores in the html


@app.route("/warehouse_form", methods = ["POST"])
def w_create():
    w = Warehouse(location=request.form['location'], store = request.form['store_choice'])
    #Warehouse is the class
    #location for Warehouse class is from html(name='location') from form

    if w.save():
        flash("flash saved")
        return redirect(url_for('warehouse'))
    else:
        return render_template('warehouse.html', name=request.args['location]'])        


@app.route("/stores")
def show_stores():
    stores  = Store.select() #passing stores from the database into 
    warehouses = Warehouse.select()
    return render_template('stores.html', stores = stores, warehouses = warehouses)

@app.route("/stores/delete/<id>", methods = ["POST"])
def destroy(id):
    # breakpoint()
    x = Store.get_by_id(id)
    
    #can use delete or delete instance

    if x.delete_instance():
        flash("Store deleted")
        return redirect(url_for('show_stores'))
    else:
        return render_template('stores.html')

@app.route("/store/<id>")
def show_stores_about(id):
    store = Store.get_by_id(id)
    #can have the 
    return render_template('stores_about.html', store = store)

@app.route("/store/<id>/edit", methods = ["POST"])
def edit(id):
    s = Store.update(name=request.form['name']).where(Store.id == id)

    #s is equal to the class with the name from the html button
    #pulling the informatino from form, not args

    if s.execute():
        flash("flash saved")
        return redirect(url_for('stores_about'))
    else:
        return render_template('store.html', name=request.args['name]'])


if __name__ == '__main__':
   app.run()