from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from . import db as database
from . models import ProductCategories, ProductItem, OrderData, CustomerUser
from flask_login import login_required, current_user,login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

routes = Blueprint('routes', __name__)

auth = Blueprint("authentication", __name__)


@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/shop', methods=['GET', 'POST'])
@login_required
def shop():
    if request.method == 'POST':
        item = ProductItem.query.all()
        ordered_quantity = float(request.form.get('ordered_quantity'))
        item_title = request.form.get('item_title')
        product_price = request.form.get('product_cost')
        total = float(product_price)*float(ordered_quantity)
        product_id = request.form.get('product_id')
        status_user = 'NC'
        user_id = current_user.user_id
        item = ProductItem.query.filter_by(product_id=product_id).first()
        item.product_quantity -= ordered_quantity
        new_order = OrderData(ordered_quantity=ordered_quantity, order_total=total,
                          order_status=status_user, customer_id=user_id, item_id=product_id, item_title=item_title, item_cost=product_price)
        database.session.add(new_order)
        database.session.commit()
        flash("Added! Continue Shopping to add more!")
        return redirect(url_for('routes.shop'))

    categories_item = ProductCategories.query.all()
    products_item = ProductItem.query.order_by(ProductItem.creation_date.desc()).all()[::-1]
    return render_template('user_shop.html', categories_item=categories_item, products_item=products_item)


@routes.route('/profile')
@login_required
def profile():
    products_item = ProductItem.query.all()
    orders_item = OrderData.query.all()
    count = 0
    for order in orders_item:
        if order.order_status == 'Purchased' and order.customer_id == current_user.user_id:
            count += 1
    return render_template('user_profile.html', user_name=current_user.user_name, orders_item=orders_item, products_item=products_item, user_id=current_user.user_id, user_username=current_user.user_handle, count=count)

@ routes.route('/search_result', methods=['GET', 'POST'])
@ login_required
def search_result():
    if request.method == 'POST':
        prod = ProductItem.query.all()
        ord = OrderData.query.all()
        quant = float(request.form.get('quant'))
        prod_name = request.form.get('prod_name')
        prod_price = request.form.get('cost')
        total = float(prod_price)*float(quant)
        prod_id = request.form.get('id')
        order_status = 'NC'
        user_id = current_user.user_id
        prod = ProductItem.query.filter_by(product_id=prod_id).first()
        prod.product_quantity -= quant
        new_order = ord(ordered_quantity=quant, order_total=total,
                          order_status=order_status, customer_id=user_id, item_id=prod_id, item_title=prod_name, item_cost=prod_price)
        database.session.add(new_order)
        database.session.commit()
        flash("Added! Continue Shopping to add more!")
        return redirect(url_for('routes.search'))
    
    search_query = request.args.get('query')
    products_item = []
    
    try:
            price = float(search_query)
            products_item = ProductItem.query.filter_by(product_price=price).all()
    except ValueError:
        # Query products by other criteria
        products_item = ProductItem.query.filter(
            (ProductItem.category.has(category_title=search_query)) |
            (ProductItem.product_name.ilike(f'%{search_query}%')) |
            (ProductItem.manufacturing_date == search_query)
        ).all()
    
    categories_item = ProductCategories.query.all()
    
    return render_template('searched_result.html', products_item=products_item, categories_item=categories_item)

@routes.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        query_search = request.form.get('query_search')
        return redirect(url_for('routes.search_result', query=query_search))

    return render_template('search_item.html')


@routes.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if request.method == 'POST':
        if 'rem' in request.form:
            order_id = int(request.form.get('rem'))
            order = OrderData.query.filter_by(order_id=order_id).first()
            if order:
                product_id = order.item_id
                product = ProductItem.query.filter_by(product_id=product_id).first()
                if product:
                    quantity = order.ordered_quantity
                    product.product_quantity += quantity
                    database.session.delete(order)
                    database.session.commit()
                    return redirect(url_for('routes.cart'))
        elif 'upd' in request.form:
            order_id = int(request.form.get('upd'))
            quantity = float(request.form.get('quant'))
            order = OrderData.query.get(order_id)
            if order:
                old_quantity = order.ordered_quantity
                order.ordered_quantity = quantity
                order.order_total = order.item_cost * order.ordered_quantity
                product = ProductItem.query.get(order.item_id)
                product.product_quantity = product.product_quantity + old_quantity - order.ordered_quantity

                database.session.commit()

                return redirect(url_for('routes.cart'))
        elif 'buyall' in request.form:
            user_id = current_user.user_id
            orders = OrderData.query.filter_by(customer_id=user_id, order_status='NC').all()

            for order in orders:
                product_id = order.item_id
                quantity = order.ordered_quantity
                product = ProductItem.query.filter_by(product_id=product_id).first()
                original_quantity = order.ordered_quantity

                if original_quantity != quantity:
                    product.product_quantity = product.product_quantity + original_quantity - quantity
                    order.ordered_quantity = quantity
                    order.order_total = quantity * order.item_cost

                order.order_status = 'Purchased'

            database.session.commit()

            return redirect(url_for('routes.cart'))

    user_id = current_user.user_id
    orders_data = OrderData.query.filter_by(customer_id=user_id, order_status='NC').all()
    total_price = 0

    for order in orders_data:
        product_id = order.item_id
        quantity = order.ordered_quantity
        product = ProductItem.query.filter_by(product_id=product_id).first()
        subtotal = quantity * order.item_cost
        total_price += subtotal

    products_item = ProductItem.query.all()

    return render_template('user_cart.html', orders_item=orders_data, products_item=products_item, user_id=current_user.user_id, total_cost=total_price)


@routes.route('/admin/manage_product', methods=['GET', 'POST'])
@login_required
def manage_product():
    if request.method == 'POST':
        if 'add_prod' in request.form:
            prod_name = request.form.get('prod_name')
            exp_date = request.form.get('exp_date')
            manu_date = request.form.get('manu_date')
            cat_id = request.form.get('cat_id')
            cost = float(request.form.get('cost'))
            unt = request.form.get('unt')
            quant = float(request.form.get('quant'))
            exp_date = datetime.strptime(exp_date, '%Y-%m-%d').date()
            manu_date = datetime.strptime(
                manu_date, '%Y-%m-%d').date()
            image = request.files['image']
            image_file = image.read()

            
            new_product = ProductItem(
                product_name=prod_name,
                expiration_date=exp_date,
                manufacturing_date=manu_date,
                product_category_id=cat_id,
                product_price=cost,
                product_unit=unt,
                product_quantity=quant,
                image_file=image_file,
                image_url=f'public/{image.filename}'
            )

            database.session.add(new_product)
            database.session.commit()
            flash('Product added successfully.', category='success')
        elif 'remove_product' in request.form:
            prod_id = request.form.get('prod_id')
            prod = ProductItem.query.get(prod_id)
            if prod:
                database.session.delete(prod)
                database.session.commit()
                flash('Product removed successfully.', category='success')
            else:
                flash('Product not found.', category='error')
        elif 'edit_prod' in request.form:
            prod_id = request.form.get('prod_id')
            prod = ProductItem.query.get(prod_id)
            if prod:
                prod.product_name = request.form.get('prod_name')
                exp_date = request.form.get('exp_date')
                manu_date = request.form.get('manu_date')
                exp_date = datetime.strptime(exp_date, '%Y-%m-%d').date()
                manu_date = datetime.strptime(
                    manu_date, '%Y-%m-%d').date()
                prod.expiration_date = exp_date
                prod.manufacturing_date = manu_date
                prod.product_category_id = request.form.get('cat_id')
                prod.product_price = float(request.form.get('cost'))
                prod.product_quantity = float(request.form.get('quant'))
                database.session.commit()
            else:
                flash('Product not found.', category='error')

        if current_user.user_role == 1:
            abort(403)
        return redirect(url_for('routes.manage_product'))

    categories_item = ProductCategories.query.all()
    products_item = ProductItem.query.all()
    return render_template('product_admin.html', categories_item=categories_item, products_item=products_item)


@routes.route('/admin_profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    if current_user.user_role == 1:
        abort(403)
    return render_template('profile_admin.html', name=current_user.user_name, user_handle=current_user.user_handle)

@routes.route('/admin', methods=['GET', 'POST'])
def admin():
    if not current_user.is_authenticated:
        return render_template('home_adm.html')
    if current_user.user_role == 1:
        return redirect(url_for('routes.index'))
    return render_template('home_adm.html')

@routes.route('/admin/manage_cat', methods=['GET', 'POST'])
@login_required
def manage_cat():
    if request.method == 'POST':
        if 'create_cat' in request.form:
            cat_name = request.form.get('create_cat')

            existing_cat = ProductCategories.query.filter_by(
                category_title=cat_name).first()
            if existing_cat:
                flash('Category already exists, Edit the category', category='error')
            else:

                cat_new = ProductCategories(category_title=cat_name)
                database.session.add(cat_new)
                database.session.commit()

        elif 'remove_cat' in request.form:
            cat_id = request.form.get('cat_id')

            cat_ = ProductCategories.query.get(cat_id)
            if cat_:
                ProductItem.query.filter_by(product_category_id=cat_id).delete()
                database.session.delete(cat_)
                database.session.commit()
                
            else:
                flash('Categor not found.', category='error')

        return redirect(url_for('routes.manage_cat'))

    if current_user.user_role == 1:
        abort(403)
    categories_item = ProductCategories.query.all()
    return render_template('manage_category_admin.html', categories_item=categories_item)

# ##############################################################################

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("routes.index"))

@auth.route("/login", methods=['GET', 'POST'])
def login():
    warnings=[]
    if request.method == 'POST':
        input_uname = request.form.get("username")
        input_pass = request.form.get("pwd")

        auth_user = CustomerUser.query.filter_by(
            user_handle=input_uname).first()
        if auth_user:
            if check_password_hash(auth_user.user_password, input_pass):
                if auth_user.user_role == 1:
                    flash("Login successful!", category='success')
                    login_user(auth_user, remember=True)
                    return redirect(url_for('routes.profile'))
            else:
                warnings.append('Incorrect password.')
        else:
            warnings.append('Username not found.')

    return render_template("user_login.html", customer_user=current_user, warnings=warnings)

@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():
    warnings=[]
    if request.method == 'POST':
        name = request.form.get("name")
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        pwdConfirm = request.form.get("confpwd")

        username_exists = CustomerUser.query.filter_by(
            user_handle=username).first()
        
        def contains_special_character(pwd):
            special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?/"
            return any(char in special_characters for char in pwd)

        if username_exists:
            warnings.append(
                'This username has already been chosen, please choose another one.')
        if pwd != pwdConfirm:
            warnings.append('Passwords do not match.')
        if len(username) < 4:
            warnings.append(
                'Please choose a longer username. Username length should be greater than 3 letters.')
        if len(pwd) < 4:
            warnings.append(
                'Please choose a longer password. Password length should be greater than 3 letters.')

        if not warnings:
            newUser = CustomerUser(user_name=name, user_handle=username, user_password=generate_password_hash(
                pwd, method='scrypt'), user_role=1)
            database.session.add(newUser)
            database.session.commit()
            login_user(newUser, remember=True)
            return redirect(url_for('routes.profile'))

    return render_template("user_signup.html", user=current_user, warnings=warnings)


# ADMIN AUTHENTICATION

@auth.route("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for("routes.admin"))

@auth.route("/admin/signup", methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        name = request.form.get("name")
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        pwdConfirm = request.form.get("confpwd")

        def contains_special_character(pwd):
            special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?/"
            return any(char in special_characters for char in pwd)

        username_exists = CustomerUser.query.filter_by(
            user_handle=username).first()

        if username_exists:
            flash(
                'This username already exist, either login or please choose another one.', category='error')
        elif pwd != pwdConfirm:
            flash('Please type the same passwords', category='error')
        elif len(username) < 5:
            flash('Length of username must be greater than 4', category='error')
        elif len(pwd) < 8:
            flash('Length of password must be greater than 7', category='error')
        elif not contains_special_character(pwd):
            flash('Please use at least one special character in your password.', category='error')
        else:
            newUser = CustomerUser(user_name=name, user_handle=username, user_password=generate_password_hash(
                pwd, method='scrypt'), user_role=0)
            database.session.add(newUser)
            database.session.commit()
            login_user(newUser, remember=True)
            flash("User created!")
            return redirect(url_for('routes.admin_profile'))

    return render_template("admin_signup.html", customer_user=current_user)


@auth.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get("admin_username")
        password = request.form.get("admin_pwd")

        user = CustomerUser.query.filter_by(user_handle=username).first()
        if user:
            if check_password_hash(user.user_password, password):
                if user.user_role == 0:
                    flash("Logged in!", category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('routes.admin'))

            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Username does not exist.', category='error')
        # Redirect back to admin login page if credentials are incorrect

    return render_template("admin_login.html", customer_user=current_user)
