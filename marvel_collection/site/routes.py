from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from marvel_collection.forms import AddMarvelCharForm
from marvel_collection.models import MarvelCharacter, db, User

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@site.route('/add', methods=['GET', 'POST'])
@login_required
def addchar():
    marvelcharform = AddMarvelCharForm()

    try:
        if request.method == 'POST' and marvelcharform.validate_on_submit():
            superhero_name = marvelcharform.superhero_name.data
            name = marvelcharform.name.data
            description = marvelcharform.description.data
            num_of_comics = marvelcharform.num_of_comics.data
            superpower = marvelcharform.superpower.data
            user_token = marvelcharform.user_token.data

            marvel_char = MarvelCharacter(superhero_name=superhero_name, name=name, 
            description=description, num_of_comics=num_of_comics, superpower=superpower, user_token=user_token)
            db.session.add(marvel_char)
            db.session.commit()

            flash(f"You have successfully added {superhero_name} to your Marvel Collection!", "char-added")
            return redirect(url_for('site.addchar'))
    except:
        raise Exception("Invalid form data. Please check your form.")

    return render_template('add.html', marvelcharform=marvelcharform)