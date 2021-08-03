import hashlib
import os
import pathlib
from collections import Iterable

from werkzeug.utils import secure_filename

from .app import app, login_manager
from flask import render_template, redirect, url_for, flash, request
from .model import Movie, Users, Ratings, Admin
from flask_login import login_user, logout_user, current_user, login_required
# from .forms import RegisterForm, LoginForm, PurchaseForm, GameForm, GameEditForm, GameDeleteForm
from .forms import LoginFormAdmin, LoginForm, RegisterForm, LibraryForm, AddUserForm, ModifyUserForm1, ModifyUserForm2, DeleteUserForm, \
    AddMovieForm, ModifyMovieForm1, ModifyMovieForm2, DeleteMovieForm, DisplayMovieRatingsForm

path = str(pathlib.Path().absolute())
UPLOADS_PATH = path+'/frontend/static/images/'

@login_manager.user_loader
def load_user(userId):
    if userId == '1234':
        return Admin.get(userId)
    return Users.get(userId)


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html", active_home="active", el=1)


@app.route("/registration", methods=['GET', 'POST'])
def registration_page():
    form = RegisterForm()
    if form.userId.data:
        if form.validate_on_submit():
            if not Users.check_userId(request.form.get('userId')):
                Users.uinsert(request.form.get('userId'), request.form.get('name'),
                              form.date.data, request.form.get('gender'), request.form.get('password'))
                flash(
                    f"Registered succesfully, Please Log In", category="success")
                return redirect(url_for('user_login_page'))
            else:
                flash('User Id already exists', category="danger")
        else:
            flash('Invalid credentials, Please try again', category="danger")

    return render_template("registration.html", form=form, active_register="active")


@app.route("/test")
def test_page():
    return render_template('test.html')


@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login_page():
    form = LoginFormAdmin()
    if form.validate_on_submit():
        admin = Admin.get(form.adminId.data)
        if Admin.check_password(form.adminId.data, form.password.data):
            login_user(admin)
            flash(
                f"Logged in Successfully!! Welcome {current_user.username}", category="success")
            return redirect(url_for('admin_page', active_login="active"))
        else:
            flash('Invalid credentials, Please try again', category="danger")
    return render_template("admin_login.html", form=form, active_admin_login="active")


@app.route("/user_login", methods=['GET', 'POST'])
def user_login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.get(form.userId.data)
        if user:
            password = form.password.data
            password = hashlib.md5(password.encode('utf8')).hexdigest()
            if user.password == password:
                login_user(user)
                flash(
                    f"Logged in Successfully!! Welcome {current_user.username}", category="success")
                return redirect(url_for('library_page'))
            else:
                flash('Invalid credentials, Please try again', category="danger")
        else:
            flash('Invalid credentials, Please try again', category="danger")
    return render_template("user_login.html", form=form, active_login="active")


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('Logged out successfully', category='info')
    #response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return redirect(url_for('home_page'))


@app.route('/user/library', methods=['GET', 'POST'])
@login_required
def library_page():
    form = LibraryForm()
    top_rec = Movie.recommendationtop()
    allmov = Movie.get_all_movies()
    if form.submit.data:
        title_movId = request.form.get('title_movId')
        print(title_movId)
        genre = request.form.get('genre')
        print(genre)
        if title_movId:
            if title_movId.isnumeric():
                print('search1')
                mov_obj = Movie.search(movieId=title_movId)
                if mov_obj:
                    if isinstance(mov_obj, Iterable):
                        return render_template("library.html", mov_obj=mov_obj, form=form, iterab=True,
                                               active_search="active")
                    else:
                        return render_template("library.html", mov_obj=mov_obj, form=form, iterab=False,
                                               active_search="active")
                else:
                    flash(f'Movie Id not found')
                    return redirect(url_for(library_page))
            else:
                print('search2')
                mov_obj = Movie.search(title=title_movId)
                if mov_obj:
                    if isinstance(mov_obj, Iterable):
                        return render_template("library.html", mov_obj=mov_obj, form=form, iterab=True,
                                               active_search="active")
                    else:
                        return render_template("library.html", mov_obj=mov_obj, form=form, iterab=False,
                                               active_search="active")
                else:
                    flash(f'Movie title not found')
                    return render_template("library.html", top_rec=top_rec, allmov=allmov, form=form, active_lib="active")
        elif genre:
            print('search3')
            sortkey = 1
            if form.selectsort.data:
                sortkey = request.form.get('selectsort')
            mov_obj = Movie.find_genre_search(genre=genre,sortkey=sortkey)
            if mov_obj:
                if isinstance(mov_obj, Iterable):
                    return render_template("library.html", mov_obj=mov_obj, form=form, iterab=True, gen=1,
                                           active_search="active")
                else:
                    return render_template("library.html", mov_obj=mov_obj, form=form, iterab=False,
                                           active_search="active")
            else:
                flash(f'Genre not found')
                return redirect(url_for('library_page'))
        else:
            flash(f"Invalid Input", category='danger')



    return render_template("library.html", top_rec=top_rec, allmov=allmov, form=form, active_lib="active")


@app.route('/movie_display/<movieId>', methods=['GET', 'POST'])
@login_required
def movie_display_page(movieId):
    form = DisplayMovieRatingsForm()
    mov_obj = Movie.search(movieId=movieId)
    rat_obj = Ratings.get_all_ratings(movieId=movieId)
    rec_obj = Movie.recommendationname(mov_obj.title)
    if form.addrating.data:
        if form.validate_on_submit():
            if Ratings.check_rating(user_id=current_user.id,movieId=movieId):
                if form.rating.data and form.review.data:
                    Ratings.rinsert(id1=current_user.id,movieid=movieId,ratings=request.form.get('rating'),reviews=request.form.get('review'))
                    flash(f'Rating entered Succesfully', category='success')
                    return render_template("displayMovie.html", movie=mov_obj, form=form, rating=rat_obj, rate= True, active_disp="active", rec_obj=rec_obj)
                else:
                    flash(f'Validation error, please try later', category='danger')
            else:
                flash(f'Validation error, please try later', category='danger')
    if form.modifyrating.data:
        if form.validate_on_submit():
            if form.rating.data and form.review.data:
                Ratings.rupdate(uid=current_user.id,movieid=movieId,ratings=request.form.get('rating'),reviews=request.form.get('review'))
                flash(f'Rating modified Succesfully', category='success')
                return render_template("displayMovie.html", movie=mov_obj, form=form, rating=rat_obj, rate= True, active_disp="active", rec_obj=rec_obj)
            else:
                flash(f'Validation error, please try later', category='danger')
    if form.deleterating.data:
        Ratings.rdelete(uid=current_user.id, movieid=movieId)
        flash(f'Rating modified Succesfully', category='success')
        return render_template("displayMovie.html", movie=mov_obj, form=form, rating=rat_obj, active_disp="active", rec_obj=rec_obj)

    if Ratings.check_rating(user_id=current_user.id,movieId=movieId):
        return render_template("displayMovie.html", movie=mov_obj, form=form, rating=rat_obj, rate= True, active_disp="active", rec_obj=rec_obj)
    return render_template("displayMovie.html", movie=mov_obj, form=form, rating=rat_obj, active_disp="active", rec_obj=rec_obj)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_page():
    if not Admin.check_password(current_user.id,current_user.password):
        flash(f'Please login as admin', category='danger')
        return redirect(url_for('admin_login_page'))
    return render_template("admin.html", active_admin="active")


# @app.route('/search')
# @login_required
# def search_display_page(title=False, genre=False):

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def admin_user_add_page():
    if not Admin.check_password(current_user.id,current_user.password):
        flash(f'Please login as admin', category='danger')
        return redirect(url_for('admin_login_page'))
    form = AddUserForm()
    print(1)
    if form.userId.data:
        print(2)
        if form.validate_on_submit():
            print(3)
            if not Users.check_userId(request.form.get('userId')):
                Users.uinsert(request.form.get('userId'), request.form.get('name'),
                              form.date.data, request.form.get('gender'), request.form.get('password'))
                flash(
                    f"User {request.form.get('userId')} added successfully", category="success")
                return redirect(url_for('admin_page'))
            else:
                flash('User Id already exists', category="danger")
        else:
            flash('Invalid credentials, Please try again', category="danger")
    return render_template("addUser.html", form=form, active_admin="active")


@app.route('/modify_user', methods=['GET', 'POST'])
@login_required
def admin_user_modify_page1():
    if not Admin.check_password(current_user.id,current_user.password):
        flash(f'Please login as admin', category='danger')
        return redirect(url_for('admin_login_page'))
    form = ModifyUserForm1()
    if form.check.data:
        user_obj = Users.ufind(request.form.get('name'))
        if user_obj:
            if isinstance(user_obj, Iterable):
                form.selectuid.choices = [(i.id, i.id) for i in user_obj]
            else:
                form.selectuid.choices = (user_obj.userId, user_obj.userId)
            return render_template("modify1User.html", form=form, active_admin="active")
        else:
            flash(f'User name not found')
            return render_template("modify1User.html", form=form, active_admin="active")
    if form.submit.data:
        return redirect(url_for("admin_user_modify_page2", userId=request.form.get('selectuid')))
    return render_template("modify1User.html", form=form, active_admin="active")

@app.route('/modify_user/<userId>', methods=['GET', 'POST'])
@login_required
def admin_user_modify_page2(userId):
    if not Admin.check_password(current_user.id,current_user.password):
        flash(f'Please login as admin', category='danger')
        return redirect(url_for('admin_login_page'))
    form = ModifyUserForm2()
    if form.validate_on_submit():
        username = request.form.get('name')
        date = form.date.data
        gender = request.form.get('gender')
        password = request.form.get('password')
        Users.uupdate(name=username, userId=userId, name1=username, dob=date, gender=gender, password=password)
        flash(f'User Details Updated',category='success')
        return render_template("modify2User.html", form=form, active_admin="active")
    else:
        flash(f'Error Please try later',category='danger')
    return render_template("modify2User.html", form=form, active_admin="active")




@app.route('/delete_user', methods=['GET', 'POST'])
@login_required
def admin_user_delete_page():
    if not Admin.check_password(current_user.id,current_user.password):
        flash(f'Please login as admin', category='danger')
        return redirect(url_for('admin_login_page'))
    form = DeleteUserForm()
    if form.check.data:
        user_obj = Users.ufind(request.form.get('name'))
        if user_obj:
            if isinstance(user_obj, Iterable):
                form.selectuid.choices = [(i.id, i.id) for i in user_obj]
            else:
                form.selectuid.choices = (user_obj.id, user_obj.id)
            return render_template("DeleteUser.html", form=form, active_admin="active")
        else:
            flash(f'User name not found')
            return render_template("deleteUser.html", form=form, active_admin="active")
    if form.submit.data:
        Users.udelete(name=request.form.get('name'), userId=request.form.get('selectuid'))
        flash(f'User deleted',category="success")
        return redirect(url_for('admin_page'))
    return render_template("deleteUser.html", form=form, active_admin="active")


@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def admin_movie_add_page():
    if not Admin.check_password(current_user.id,current_user.password):
        flash(f'Please login as admin', category='danger')
        return redirect(url_for('admin_login_page'))
    form = AddMovieForm()
    print(1)
    if form.movieId.data:
        print(2)
        if form.validate_on_submit():
            print(3)
            print(Movie.check_movieId(request.form.get('movieId')))
            if not Movie.check_movieId(request.form.get('movieId')):
                print(4)
                image = request.files.get('imageupload')
                print(5)
                image.save(os.path.join(UPLOADS_PATH, request.form.get('movieId')+'.jpg'))
                print(5)
                Movie.minsert(request.form.get('movieId'), request.form.get('title'),UPLOADS_PATH,
                              request.form.get('description'),request.form.get('genre'))
                flash(
                    f"User {request.form.get('title')} added successfully", category="success")
                return redirect(url_for('admin_page'))
            else:
                flash('Movie Id already exists', category="danger")
        else:
            flash('Invalid credentials, Please try again', category="danger")
    return render_template("addMovie.html", form=form, active_admin="active")


@app.route('/modify_movie', methods=['GET', 'POST'])
@login_required
def admin_movie_modify_page1():
    if not Admin.check_password(current_user.id,current_user.password):
        flash(f'Please login as admin', category='danger')
        return redirect(url_for('admin_login_page'))
    form = ModifyMovieForm1()
    if form.check.data:
        mov_obj = Movie.find_genre(request.form.get('genre'))
        if mov_obj:
            if isinstance(mov_obj, Iterable):
                form.selectmid.choices = [(i.movieId, i.movieId) for i in mov_obj]
            else:
                form.selectmid.choices = (mov_obj.movieId, mov_obj.movieId)
            return render_template("modify1Movie.html", form=form, active_admin="active")
        else:
            flash(f'Genre not found')
            return render_template("modify1Movie.html", form=form, active_admin="active")
    if form.submit.data:
        return redirect(url_for("admin_movie_modify_page2", movieId=request.form.get('selectmid')))
    return render_template("modify1Movie.html", form=form, active_admin="active")

@app.route('/modify_movie/<movieId>', methods=['GET', 'POST'])
@login_required
def admin_movie_modify_page2(movieId):
    if not Admin.check_password(current_user.id,current_user.password):
        flash(f'Please login as admin', category='danger')
        return redirect(url_for('admin_login_page'))
    form = ModifyMovieForm2()
    print(1)
    print(form.validate_on_submit())
    print(form.errors.items())
    if form.validate_on_submit():
        print(1)
        image = request.files.get('imageupload')
        print(1)
        image.save(os.path.join(UPLOADS_PATH, str(movieId) + '.jpg'))
        print(1)
        Movie.mupdate(movieId, request.form.get('title'), UPLOADS_PATH,
                      request.form.get('description'), request.form.get('genre'))
        print(1)
        flash(
            f"User {request.form.get('title')} modified successfully", category="success")
        return redirect(url_for('admin_page'))
    else:
        flash(f'Error Please try later',category='danger')
    return render_template("modify2Movie.html", form=form, active_admin="active")


@app.route('/delete_movie', methods=['GET', 'POST'])
@login_required
def admin_movie_delete_page():
    if not Admin.check_password(current_user.id,current_user.password):
        flash(f'Please login as admin', category='danger')
        return redirect(url_for('admin_login_page'))
    form = DeleteMovieForm()
    if form.check.data:
        mov_obj = Movie.find_genre(request.form.get('genre'))
        if mov_obj:
            if isinstance(mov_obj, Iterable):
                form.selectmid.choices = [(i.movieId, i.movieId) for i in mov_obj]
            else:
                form.selectmid.choices = (mov_obj.movieId, mov_obj.movieId)
            return render_template("deleteMovie.html", form=form, active_admin="active")
        else:
            flash(f'User name not found')
            return render_template("deleteMovie.html", form=form, active_admin="active")
    if form.submit.data:
        Movie.mdelete(genre=request.form.get('genre'), movieId=request.form.get('selectmid'))
        flash(f'Movie deleted',category="success")
        return redirect(url_for('admin_page'))
    return render_template("deleteMovie.html", form=form, active_admin="active")
