from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task


@app.route("/")
def home():
    return render_template("tasks.html")


@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories) #1st 'categories' = is the variable name we can use within the HTML template, 2nd is the list defined infunction above (shows why it's important to name similarly)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST": # step 2 - checks if the request (submit btn) is a POST request. If yes, the data is posted to specified location
        category = Category(category_name=request.form.get("category_name")) # specified location
        db.session.add(category) 
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html") # step 1 - uses default 'GET' and renders add category template. 
# consider adding defensive programming to handle brute-force attacks and some error handling


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id) #attempts to find the specified record using the data provided, and if no match is found, it will trigger a 404 error page.
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))