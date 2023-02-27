from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    # show all recipes
    recipe_list = Recipe.query.all()
    print([recipe.id for recipe in recipe_list])
    return render_template('base.html', recipe_list=recipe_list)

@app.route('/add', methods=["POST"])
def add():
    title = request.form.get("title")
    new_recipe = Recipe(title=title, complete=False)
    db.session.add(new_recipe)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/complete/<int:recipe_id>')
def complete(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    recipe.complete = not recipe.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int:recipe_id>')
def delete(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # new_todo = Recipe(title="Recipe 1", complete=False)
        # db.session.add(new_todo)
        # db.session.commit()   
        app.run(debug=True, use_reloader=False)
    # enable with flask --debug run