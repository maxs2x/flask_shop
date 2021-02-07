import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from user_login import UserLogin
from admin.admin import admin

UPLOAD_FOLDER = 'static/downloads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIUONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_6#y2L"F4h8z\n\aec]/'
app.register_blueprint(admin, url_prefix='/admin')
login_manager = LoginManager(app)

db = SQLAlchemy(app)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String)
    producer = db.Column(db.String)
    model_auto = db.Column(db.String, nullable=False)
    navigation_categories = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    image_alt = db.Column(db.String)

    def __repr__(self):
        return self.description


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=True)
    data = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return Users.query.get(int(user_id))


def redirect_for_subpath(subpath, request):
    print(request.method)
    cart_informations = cart_info(session)
    if request.method == 'GET':
        items = Products.query.filter_by(navigation_categories=str(subpath))
        for elem in items:
            print(elem)
        return render_template('list_products.html', data=items, cart_info=cart_informations)
    elif request.method == 'POST':
        session.modified = True
        items = Products.query.filter_by(navigation_categories=str(subpath))
        return render_template('list_products.html', data=items, cart_info=cart_informations)


def cart_info(session):
    if not session.get('cart'):
        return [0, 0]
    content_cart = session['cart']
    count_product = 0
    cost_products_in_cart = 0
    id_product_in_cart = []
    for product in content_cart:
        id_product_in_cart.append(int(product['product_id']))
        count_product += int(product['value'])
        items = Products.query.filter_by(id=str(product['product_id']))
        cost_products_in_cart += int(items[0].price) * int(product['value'])
    info = {'count_product': count_product, 'cost_products_in_cart': cost_products_in_cart, 'arr_product_in_cart': id_product_in_cart}
    print(info)
    return info


@app.route('/')
def index():
    items = Products.query.all()
    cart_informations = cart_info(session)
    return render_template('index.html', data=items, cart_info=cart_informations)


@app.route('/<path:subpath>')
def route_first_level_path(subpath):
    cart_informations = cart_info(session)
    if subpath == 'about':
        return render_template('about.html', cart_info=cart_informations)
    elif subpath == 'electrical':
        return render_template('electrical.html', cart_info=cart_informations)
    elif subpath == 'brake':
        return render_template('brake.html', cart_info=cart_informations)
    elif subpath == 'engine':
        return render_template('engine.html', cart_info=cart_informations)
    elif subpath == 'body':
        return render_template('body.html', cart_info=cart_informations)
    elif subpath == 'transmission':
        return render_template('transmission.html', cart_info=cart_informations)
    elif subpath == 'suspension':
        return render_template('suspension.html', cart_info=cart_informations)
    elif subpath == 'contacts':
        return render_template('contacts.html', cart_info=cart_informations)


def do_in_cart(id_product, session):
    # приводим оба параметра к числу что бы сессия не материлась
    id = id_product
    value = int('1')
    # cart_session() # проверяет существует ли сессия корзины и если нет, то создает её, а если да, то норм
    if not session.get('cart'):
        session['cart'] = [{
            'product_id': id,
            'value': int(value)
        }]
    else:
        # добавляем товар к сессии в виде словаряa
        a = 0
        for elem in session['cart']:
            a += 1
            if int(elem['product_id']) == int(id):
                session['cart'].remove(elem)
                elem['value'] = elem['value'] + int(1)
                session['cart'].append(elem)
                session.modified = True
                break
            if a == len(session['cart']):
                session['cart'].append({
                    'product_id': id,
                    'value': int(value)
                })
                session.modified = True
                break
    in_cart = product_in_cart(session)
    print(session['cart'])
    cart_informations = cart_info(session)
    return render_template('cart.html', session=session, data=in_cart, cart_info=cart_informations)


@app.route('/<variable_name>/<path:subpath>', methods=['POST', 'GET'])
def categories_menu(variable_name, subpath):
    request_path = request
    if request.method == 'POST':
        do_in_cart(request.form['add_id'], session)
    display = redirect_for_subpath(subpath, request_path)
    return display


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        balance = request.form['balance']
        description = request.form['description']
        producer = request.form['producer']
        model_auto = request.form['model_auto']
        navigation_categories = request.form['navigation_categories']
        file = request.files['file']
        image_alt = request.form['image_alt']
        filename = str()
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        item = Products(title=title, price=price, balance=balance, description=description, producer=producer,
                        model_auto=model_auto, navigation_categories=navigation_categories, image=filename, image_alt=image_alt)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('create'))
        except:
            return 'ERROR in DB'
    else:
        return render_template('create.html')


def product_in_cart(session):
    product_in_cart = []
    for elem in session['cart']:
        product_info = dict()
        items = Products.query.filter_by(id=str(elem['product_id']))
        product_info['price'] = int(items[0].price)
        product_info['title'] = items[0].title
        product_info['id'] = elem['product_id']
        product_info['value'] = int(elem['value'])
        product_info['producer'] = items[0].producer
        product_info['image'] = items[0].image
        product_in_cart.append(product_info)
        print(product_in_cart)
    return product_in_cart


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    cart_informations = cart_info(session)
    if not session.get('cart'):
        return render_template('cart.html', cart_info=cart_informations)
    if request.method == 'GET':
        in_cart = product_in_cart(session)
        return render_template('cart.html', data=in_cart, cart_info=cart_informations)
    else:
        if 'del_id' in request.form:
            id = request.form['del_id']
            a = 0
            for elem in session['cart']:
                if elem['product_id'] == id:
                    del session['cart'][a]
                    in_cart = product_in_cart(session)
                    if len(in_cart) > 0:
                        del in_cart[a]
                a += 1
        elif ('add_one_id' in request.form) or ('del_one_id' in request.form):
            if 'add_one_id' in request.form:
                operation = int(1)
                print(operation)
                id = request.form['add_one_id']
            elif 'del_one_id' in request.form:
                operation = int(-1)
                id = request.form['del_one_id']
            a = 0
            print(operation)
            for elem in session['cart']:
                if elem['product_id'] == id:
                    session['cart'][a]['value'] += operation
                    if session['cart'][a]['value'] == 0:
                        del session['cart'][a]
                    break
                a += 1
        in_cart = product_in_cart(session)
        cart_informations = cart_info(session)
        session.modified = True
        return redirect(url_for('cart'))



@app.route('/add-to-cart/<id_product>', methods=['GET', 'POST'])
def add_to_cart(id_product):
    template = do_in_cart(id_product, session)
    return template


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()
        print(user.password)
        print(generate_password_hash(password))
        print(user.id)
        if check_password_hash(str(user.password), str(password)):
            login_user(user, remember=True)
            cart_informations = cart_info(session)
            return render_template('/profile.html', name=user.name, cart_info=cart_informations)

    cart_informations = cart_info(session)
    return render_template('login.html', cart_info=cart_informations)


@app.route('/profile')
@login_required
def profile():
    cart_informations = cart_info(session)
    return render_template('profile.html', name=current_user.name, cart_info=cart_informations)


@app.route('/test')
def teat():
    return render_template('test.html')


@app.route('/test2')
def test():
    cart_informations = cart_info(session)
    return render_template('test2.html', cart_info=cart_informations)


@app.route('/logout')
@login_required
def logout():
    cart_informations = cart_info(session)
    logout_user()
    return render_template('login.html', cart_info=cart_informations)


def validation_name(name):
    status_validation = False
    if 3 < len(str(name)) < 20:
        if name[0].isalpha():
            status_validation = True
            return status_validation
        else:
            print('Имя должно начинаться с буквы')
            return status_validation
    else:
        print('Имя должно содержать от 4 до 20 символов')


def validation_email(email):
    if len(str(email)) > 6:
        if '@' in email and '.' in email:
            if email[0] != '@' or email[:-1] != '@':
                user = Users.query.filter(Users.email == email).first()
                if not user:
                    return True
                else:
                    return 'Пользователь с таким e-mail уже зарегистрирован'
            else:
                return 'Неверно введен e-mail'
        else:
            return 'Неверно введен e-mail'
    else:
        return 'Неверно введен e-mail'


def validation_phone(phone):
    if len(phone) == 10:
        user = Users.query.filter(Users.phone == phone).first()
        if not user:
            return True
        else:
            return 'Пользователь с таким номером телефона уже зарегистрирован'


def validation_password(password_1, password_2):
    if password_1 == password_2:
        if 5 < len(str(password_1)) < 30:
            if any([x.isupper() for x in password_1]):
                if any([x.isdigit() for x in password_1]):
                    return True
                else:
                    return 'Пароль дожен содержать хотя бы одну цифру'
            else:
                return 'Пароль должен содержать хотя бы одну заглавную букву'
        else:
            return 'Пароль не должен быть короче 6 символов'
    return 'Пароли должны совпадать'


def validation_registration(name, email, password_1, password_2, phone):
    result_name = validation_name(name)
    result_email = validation_email(email)
    result_password = validation_password(password_1, password_2)
    result_phone = validation_phone(phone)
    status = True if result_name == True and result_email == True and result_password == True and result_phone == True else False
    result = {
        'status_validation': status,
        'name':  result_name,
        'email': result_email,
        'password': result_password,
        'phone': result_phone
        }
    print(result)
    return result



@app.route('/registration', methods=['GET', 'POST'])
def registration():
    cart_informations = cart_info(session)
    if request.method == 'GET':
        return render_template('registration.html', cart_info=cart_informations)
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        print(phone)
        validation = validation_registration(name, email, request.form['password'], request.form['password2'], phone)
        if validation['status_validation']:
            hash = generate_password_hash(request.form['password'])
            new_user = Users(name=name, email=email, password=hash, data='2021', phone=phone)
            try:
                db.session.add(new_user)
                db.session.flush()
                db.session.commit()
                return render_template('login.html', cart_info=cart_informations)
            except:
                db.session.rollback()
                print('Error ad in db')
                return render_template('registration.html', cart_info=cart_informations)
        else:
            for x in validation:
                if type(validation[x]) != type(True):
                    flash(validation[x])
                    return render_template('registration.html', cart_info=cart_informations)
                else:
                    flash('Error')
                    return render_template('registration.html', cart_info=cart_informations)


if __name__ == "__main__":
    app.run(debug=True)
