from flask import render_template, flash, request, redirect, url_for
import requests
from .forms import SearchForm
from flask_login import login_required, current_user
from .import bp as main
from .models import Pokemon, Comment
from app.blueprints.auth.models import User
from app import db

@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/pokemon', methods=['GET','POST'])
@login_required
def pokemon():
    pokemon_name = None
    form = SearchForm()
    # Validate Form
    if form.validate_on_submit():
        pokemon_name = form.pokemon_name.data.lower()
        form.pokemon_name.data = '' #clear form after hitting search
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        if response.ok:
            data = response.json()
            if not data:
                flash("Something went wrong. Couldn't connect the library.",'danger')
                return render_template("pokemon.html.j2", form=form)
            
            pokemon_dict = {  
                'name': data['name'],
                'ability': data['abilities'][0]['ability']['name'],
                'experience': data['base_experience'],
                'image_url': data['sprites']['other']['dream_world']['front_default'],
                'sprite_url': data['sprites']['front_shiny']
                }
            #check if the searched pokemon exists in the database
            if Pokemon.query.filter_by(name=pokemon_name).first() is None:
                new_poke = Pokemon(**pokemon_dict)
                new_poke.save()
                new_poke.owners.append(current_user) #record this user has catched this poke in the "catched" table
                db.session.commit()
            else:
                Pokemon.query.filter_by(name=pokemon_name).first().owners.append(current_user)   
                db.session.commit() 
                           
            return render_template("pokemon.html.j2", form=form, pokemon = pokemon_dict)
        flash(f'There is no pokemon named {pokemon_name}','warning')
        return render_template("pokemon.html.j2", form=form)
    return render_template('pokemon.html.j2', form=form)


@main.route('/show_pokemons', methods=['GET'])
@login_required
def show_pokemons():
    pokemons = Pokemon.query.all()
    return render_template('catched_poke.html.j2',pokemons=pokemons)

"""
@main.route('/posts', methods=['GET', 'POST'])
@login_required
def show_pokemons():
    if request.method == 'POST':
        body_from_form = request.form.get('body')
        try:
            new_comment = Comment(body=body_from_form, user_id=current_user.id)
            new_comment.save()
            flash("Your comment has been posted successfully", "success")
        except:
            flash("Error Creating Post.  Try again!", "danger")
  
    #return render_template('index.html.j2')
"""

@main.route('/show_pokemons', methods=['GET', 'POST'])
@login_required
def comment():
    if request.method == 'POST':
        body_from_form = request.form.get('body')
        pokemon_id = request.args.get('id')
        try:
            new_comment = Comment(body=body_from_form, user_id=current_user.id, pokemon_id=pokemon_id)
            new_comment.save()
            flash("Your comment has been posted successfully. Click your 'bell' to see all the comments.", "success")
        except:
            flash("There was an error while posting your comment. Please try agian!", "danger")
    pokemons = Pokemon.query.all()
    return render_template('/catched_poke.html.j2',pokemons=pokemons)

@main.route('/show_comments', methods=['GET', 'POST'])
@login_required
def show_comments():
    comments = Comment.query.all()
    return render_template('show_comments.html.j2',comments=comments)

@main.route('/delete_comment/<int:id>', methods=['GET'])
@login_required
def delete_comment(id):
    comment_to_delete = Comment.query.get(id)
    if current_user.id==comment_to_delete.user_id:
        comment_to_delete.delete()
        flash("Your post has been deleted", "info")
    else:
        flash("Get outta here you hacker!!!!","danger")
    return redirect(url_for('main.show_comments'))

