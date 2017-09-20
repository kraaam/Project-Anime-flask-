from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

import bs4 as bs
import urllib

from flask_whooshalchemy import whoosh_index

from . import admin
from forms import AnimeForm, ParseAnimeForm
from .. import db
from ..models import Anime

def check_admin():
    if not current_user.is_admin:
        abort(403)


@admin.route('/animes', methods=['GET', 'POST'])
@login_required
def list_animes():

    check_admin()

    animes = Anime.query.all()

    return render_template('admin/animes/animes.html',
                           animes=animes, title="Animes")
@admin.route('/search')
def search():
    animes = Anime.query.whoosh_search(request.args.get('query')).all()

    if len(animes)>1:
        return render_template('admin/animes/animes.html',
                               animes=animes, title="Animes")
    else:
        recommendation = ''
        current_anime = ''
        for anime in animes:
            print anime.genres
            current_anime = anime.title
            recommendation = anime.genres

        print ('ANIME GENRES: ' + recommendation)
        recommendations = Anime.query.whoosh_search(recommendation).all()

        index = 0
        for anime_recommendation in recommendations:
            if current_anime == anime_recommendation.title:
                recommendations.pop(index)
            index += 1

        length = len(recommendation)
        # recommendations.pop(0)
        return render_template('admin/animes/animes.html',
                                   animes=animes, recommendation=recommendations, title="Anime")

    # if request.args.get('query') != '':
    #     animes = Anime.query.whoosh_search(request.args.get('query')).all()
    #
    #     return render_template('admin/animes/animes.html',
    #                            animes=animes, title="Animes")
    # else:
    #     list_animes()

@admin.route('/animes/parse-anime', methods=['GET', 'POST'])
@login_required
def parse_anime():
    check_admin()
    form = ParseAnimeForm()

    if form.validate_on_submit():
        link = form.url.data
        sauce = urllib.urlopen(link).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')

        title = soup.find('span', attrs={"itemprop": "name"}).string

        image2 = soup.find('img', class_="ac", attrs={"itemprop": "image"})
        image = image2.get('src')

        genre = soup.find('span', text="Genres:", attrs={'class': 'dark_text'})
        parent = genre.parent
        genres = parent.findAll('a')
        genres_append = ""
        genre_list = []
        for list in genres:
            genres_append += list.text + ', '
            genre_list.append(str(list.text))
        list_genres = str(genres_append)


        try:
            studio = soup.find('span', text="Studios:", attrs={'class': 'dark_text'})
            studios_parent = studio.parent
            studios = studios_parent.findAll('a')
            studios_list = ""
            for list in studios:
                studios_list += list.text + ', '
            list_studios = (studios_list)

        except:
            list_studios = 'None'


        sypnosis = soup.find('span', attrs={"itemprop": "description"})
        sypnosis2 = sypnosis.text
        sypnosiss = repr(sypnosis2)

        anime = Anime(title=title,
                      sypnosis=sypnosiss,
                      genres=list_genres,
                      studios=list_studios,
                      imagesrc=image)
        try:
            db.session.add(anime)
            db.session.commit()
            flash('You have successfully added ' + title)
        except:
             flash('Error: ' + title + ' already exists in the database.')

        return redirect(url_for('admin.list_animes'))


    return render_template('admin/animes/parse_anime.html', form=form, title="Parse")

@admin.route('/animes/add', methods=['GET', 'POST'])
@login_required
def add_anime():

    check_admin()

    add_anime = True

    form = AnimeForm()
    if form.validate_on_submit():
        anime = Anime(title=form.title.data,
                        sypnosis=form.sypnosis.data,
                        genres=form.genres.data)
        try:
            db.session.add(anime)
            db.session.commit()
            flash('You have successfully added ' + form.title.data)
        except:
            flash('Error: ' + form.title.data + ' already exists in the database.')

        return redirect(url_for('admin.list_animes'))

    return render_template('admin/animes/anime.html', action="Add",
                           add_anime=add_anime, form=form,
                           title="Add Anime")


@admin.route('/animes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_anime(id):
    check_admin()

    add_anime = False

    anime = Anime.query.get_or_404(id)
    form = AnimeForm(obj=anime)
    if form.validate_on_submit():
        anime.title = form.title.data
        anime.sypnosis = form.sypnosis.data
        anime.genres = form.genres.data
        # anime.studios = form.Studios.data
        db.session.commit()
        flash('You have successfully edited ' + form.title.data)

        return redirect(url_for('admin.list_animes'))

    form.title.data = anime.title
    form.sypnosis.data = anime.sypnosis
    form.genres.data = anime.genres
    return render_template('admin/animes/anime.html', action="Edit",
                           add_anime=add_anime, form=form,
                           anime=anime, title="Edit Anime")


@admin.route('/animes/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_anime(id):

    check_admin()

    anime = Anime.query.get_or_404(id)
    db.session.delete(anime)
    db.session.commit()
    flash('Anime has successfully deleted')

    return redirect(url_for('admin.list_animes'))

    return render_template(title="Delete Anime")