from flask import render_template, redirect
from form import RegisterForm, EditUserForm, LoginForm, RatingForm, CommentForm
from form import AddFood
from model import User, NewProduct, Rating, Comment, Like, Dislike
from ext import app, db
from flask_login import login_user, logout_user, current_user, login_required

from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash

city_info = {
    'Tbilisi': {
        'image': 'tbilisi.png',
        'population': '1.1 million',
        'landmark': 'Narikala Fortress',
        'fun_fact': 'Tbilisi means "warm place" in Georgian, due to the area\'s numerous sulfuric hot springs.'
    },
    'Batumi': {
        'image': 'batumi.png',
        'population': '155,000',
        'landmark': 'Batumi Boulevard',
        'fun_fact': 'Batumi is known for its unique architecture, blending traditional and modern styles.'
    },
    'Telavi': {
        'image': 'telavi.png',
        'population': '21,800',
        'landmark': 'Batonis Tsikhe Fortress',
        'fun_fact': 'Telavi is the heart of Georgia’s wine region, Kakheti.'
    },
    'Tusheti': {
        'image': 'tusheti.png',
        'population': 'less than 1,000',
        'landmark': 'Omalo Fortress',
        'fun_fact': 'Tusheti is known for its stunning natural landscapes and traditional stone towers.'
    },
    'Kutaisi': {
        'image': 'kutaisi.png',
        'population': '147,000',
        'landmark': 'Bagrati Cathedral',
        'fun_fact': 'Kutaisi is one of the oldest continuously inhabited cities in the world.'
    },
    'Rustavi': {
        'image': 'rustavi.png',
        'population': '125,000',
        'landmark': 'Rustavi Metallurgical Plant',
        'fun_fact': 'Rustavi was developed as a major industrial center during the Soviet era.'
    },
    'Gori': {
        'image': 'gori.png',
        'population': '48,000',
        'landmark': 'Stalin Museum',
        'fun_fact': 'Gori is the birthplace of Joseph Stalin, the Soviet leader.'
    },
    'Zugdidi': {
        'image': 'zugdidi.png',
        'population': '42,000',
        'landmark': 'Dadiani Palace',
        'fun_fact': 'Zugdidi is known for the Dadiani Palace, home to one of Georgia’s most important noble families.'
    },
    'Poti': {
        'image': 'poti.png',
        'population': '41,500',
        'landmark': 'Poti Cathedral',
        'fun_fact': 'Poti is a major port city on the Black Sea.'
    },
    'Kobuleti': {
        'image': 'kobuleti.png',
        'population': '20,000',
        'landmark': 'Kobuleti Beach',
        'fun_fact': 'Kobuleti is a popular seaside resort known for its beaches and subtropical climate.'
    },
    'Samtredia': {
        'image': 'samtredia.png',
        'population': '25,300',
        'landmark': 'St. Nino Church',
        'fun_fact': 'Samtredia is an important railway hub in Georgia.'
    },
    'Senaki': {
        'image': 'senaki.png',
        'population': '27,800',
        'landmark': 'Senaki Theater',
        'fun_fact': 'Senaki has a vibrant cultural scene, with its theater being a central attraction.'
    },
    'Zestafoni': {
        'image': 'zestafoni.png',
        'population': '25,000',
        'landmark': 'Zestafoni Metallurgical Plant',
        'fun_fact': 'Zestafoni is known for its large ferroalloy plant.'
    },
    'Akhaltsikhe': {
        'image': 'axalcixe.png',
        'population': '17,300',
        'landmark': 'Rabati Castle',
        'fun_fact': 'Akhaltsikhe means "new castle" in Georgian.'
    },
    'Ozurgeti': {
        'image': 'ozurgeti.png',
        'population': '20,600',
        'landmark': 'Ozurgeti Museum',
        'fun_fact': 'Ozurgeti is the administrative center of the Guria region.'
    },
    'Kaspi': {
        'image': 'kaspi.png',
        'population': '14,700',
        'landmark': 'Kaspi Cement Factory',
        'fun_fact': 'Kaspi is known for its large cement factory, which is one of the largest in the region.'
    }
}








@app.route("/")

def index():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")



@app.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/explore")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/register", methods=["GET","POST"])

def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(User.username == form.username.data).first()
        if existing_user is None:
            if form.profile_image.data:
                profile_image = form.profile_image.data
                path = f"{app.root_path}\static\{profile_image.filename}"
                profile_image.save(path)
                new_user = User(path = profile_image.filename ,username=form.username.data, gender=form.gender.data, email=form.email.data, password=form.password.data, birthday=form.birthday.data, )
                db.session.add(new_user)
                db.session.commit()
                return redirect("/login")
        else:
            form.username.errors.append("Username already exists. Please choose a different one.")

    return render_template("register.html", form=form)

@app.route("/registered_users")
@login_required
def registered():
    registered_users = User.query.all()
    return render_template("users.html", registered_users=registered_users)


@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    user = User.query.get(user_id)
    form = EditUserForm(username=user.username, email=user.email, password=user.password, birthday=user.birthday, path=user.path)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:
            user.password = generate_password_hash(form.password.data)
        user.birthday = form.birthday.data

        if form.profile_image.data:
            profile_image = form.profile_image.data
            path = f"{app.root_path}\static\{profile_image.filename}"
            profile_image.save(path)
            user.path = profile_image.filename

        db.session.commit()
        return redirect("/registered_users")

    return render_template("edit_user.html", form=form)


@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/")




@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    add = AddFood()
    if add.validate_on_submit():
        if add.image.data:
            image = add.image.data
            image_path = f"{app.root_path}\static\{image.filename}"
            image.save(image_path)


        new = NewProduct(image_path=image.filename, name=add.name.data, description=add.description.data, country=add.country.data, address=add.address.data, price=add.price.data, author=current_user.username)

        db.session.add(new)
        db.session.commit()
        return redirect("/explore")

    return render_template("add.html", add=add)


@app.route("/explore")

def explore():
    create = NewProduct.query.all()
    return render_template("explore.html", create=create)




@app.route("/edit_food/<int:food_id>", methods=["GET", "POST"])
def edit_food(food_id):
    edit = NewProduct.query.get(food_id)
    add = AddFood(image_path=edit.image_path,name=edit.name, description=edit.description, country=edit.country, address=edit.address, price = edit.price)
    if add.validate_on_submit():
        edit.name = add.name.data
        edit.description = add.description.data
        edit.country = add.country.data
        edit.address = add.address.data
        edit.price = add.price.data
        if add.image.data:
            image = add.image.data
            image_path = f"{app.root_path}\static\{image.filename}"
            image.save(image_path)
            edit.image_path = image.filename


        db.session.commit()
        return redirect("/explore")
    return render_template("editfood.html", add=add)

@app.route("/delete_food/<int:food_id>", )
def delete_food(food_id):
    washla = NewProduct.query.get(food_id)
    db.session.delete(washla)
    db.session.commit()

    return redirect("/explore")



@app.route("/product/<int:product_id>", methods=["GET", "POST"])
@login_required
def product(product_id):
    product = NewProduct.query.get(product_id)

    form = RatingForm()
    comment_form = CommentForm()

    if form.validate_on_submit():
        rating = Rating(product_id=product.id, rating=form.rating.data)
        db.session.add(rating)
        db.session.commit()

        return redirect(f"/product/{product.id}")


    if comment_form.validate_on_submit():
        comment = Comment(product_id=product.id, comment=comment_form.comment.data, author = current_user.username)
        db.session.add(comment)
        db.session.commit()

        return redirect(f"/product/{product.id}")

    avg_rating = db.session.query(func.avg(Rating.rating)).filter(Rating.product_id == product_id).scalar()
    avg_rating = round(avg_rating, 2) if avg_rating else 'N/A'

    comments = Comment.query.filter_by(product_id=product_id).all()

    comment_count = Comment.query.filter_by(product_id=product_id).count()
    rating_count = Rating.query.filter_by(product_id=product_id).count()
    like_count = Like.query.filter_by(product_id=product_id).count()
    dislike_count = Dislike.query.filter_by(product_id=product_id).count()

    formatted_created_at = product.created_at.strftime('%Y-%m-%d %H:%M:%S')

    return render_template("product.html", product=product, form=form, avg_rating=avg_rating, comment_form=comment_form, comments = comments, comment_count = comment_count, rating_count = rating_count, formatted_created_at=formatted_created_at, like_count=like_count, dislike_count=dislike_count)


@app.route("/delete_comment/<int:comment_id>")
def delete_comments(comment_id):
    comment = Comment.query.get(comment_id)
    product_id = comment.product_id
    db.session.delete(comment)
    db.session.commit()

    return redirect(f"/product/{product_id}")

@app.route("/edit_comment/<int:comment_id>", methods=["GET", "POST"])
def edit_comments(comment_id):
    edit_comment = Comment.query.get(comment_id)
    product_id = edit_comment.product_id
    edit = CommentForm(comment=edit_comment.comment)
    if edit.validate_on_submit():
        edit_comment.comment = edit.comment.data

        db.session.commit()
        return redirect(f"/product/{product_id}")

    return render_template("editcomment.html", edit=edit)


@app.route('/like/<int:product_id>', methods=['POST'])
def like_product(product_id):
    existing_like = Like.query.filter_by(product_id=product_id, user_id=current_user.id).first()
    if existing_like is None:
        like = Like(product_id=product_id, user_id=current_user.id)
        db.session.add(like)

        existing_dislike = Dislike.query.filter_by(product_id=product_id, user_id=current_user.id).first()
        if existing_dislike:
            db.session.delete(existing_dislike)
        db.session.commit()
    else:
        db.session.delete(existing_like)
        db.session.commit()
    return redirect(f"/product/{product_id}")


@app.route('/dislike/<int:product_id>', methods=['POST'])
def dislike_product(product_id):
    existing_dislike = Dislike.query.filter_by(product_id=product_id, user_id=current_user.id).first()
    if existing_dislike is None:
        dislike = Dislike(product_id=product_id, user_id=current_user.id)
        db.session.add(dislike)

        existing_like = Like.query.filter_by(product_id=product_id, user_id=current_user.id).first()
        if existing_like:
            db.session.delete(existing_like)
        db.session.commit()

    else:
        db.session.delete(existing_dislike)
        db.session.commit()
    return redirect(f"/product/{product_id}")



@app.route("/destinations")
def destinations():


    cities = db.session.query(NewProduct.country, db.func.count(NewProduct.id).label('product_count')).group_by(
        NewProduct.country).order_by(db.desc('product_count')).all()
    return render_template("destinations.html", cities = cities, city_info=city_info)



@app.route("/products_by_city/<city>")
def products_by_city(city):
    products = NewProduct.query.filter_by(country=city).all()
    return render_template("products_by_city.html", products=products, city = city)