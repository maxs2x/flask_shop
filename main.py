import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

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
db.init_app(app)


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


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=True)
    data = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer, nullable=False)


class HistorySells(db.Model):
    user_email = db.Column(db.String, primary_key=True)
    id_product = db.Column(db.String, nullable=True)
    history = db.Column(db.String, nullable=True)
    order_status = db.Column(db.String, nullable=True)
    last_order = db.Column(db.String, nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


def redirect_for_subpath(subpath, request):
    cart_informations = cart_info(session)
    if request.method == 'GET':
        items = Products.query.filter_by(navigation_categories=str(subpath))
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
        cost_products_in_cart += transformation_in_int(items[0].price) * transformation_in_int(product['value'])
    info = {'count_product': count_product, 'cost_products_in_cart': cost_products_in_cart, 'arr_product_in_cart': id_product_in_cart}
    return info


def bread_crumbs(url, elem):
    menu_categories = {'Кузов': ['front_bumper'], 'Элуктрика': ['gena']}
    if elem:
        navigation_categories = elem['navigation_categories']
        for item in menu_categories:
            if navigation_categories in item:
                x = navigation_categories
                return x

@app.route('/')
def index():
    items = Products.query.all()
    carts_information = cart_info(session)
    return render_template('index.html', data=items[0: 11], cart_info=carts_information, main=[1, 2])


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
    elif subpath == 'where':
        return render_template('where.html', cart_info=cart_informations)
    elif subpath == 'why':
        return render_template('why.html', cart_info=cart_informations)


def quantity_validation(id_product, value_in, value_add):
    items = Products.query.filter_by(id=str(id_product))

    if (int(value_add) + int(value_in)) <= transformation_in_int(items[0].balance):
        if (int(value_add) + int(value_in)) > -1:
            print('quantity_validation')
            return True
        print('quantity_validation FALSE')
        return False
    else:
        print('quantity_validation FALSE')
        return False


def do_in_cart(id_product, session, *args):
    # приводим оба параметра к числу что бы сессия не материлась
    id = id_product
    if len(args) > 0:
        value = int(args[0])
    else:
        value = int('1')
    # проверяет существует ли сессия корзины и если нет, то создает её, а если да, то норм
    if not session.get('cart'):
        validation_value = quantity_validation(id_product, 0, value)
        if validation_value:
            session['cart'] = [{
                'product_id': id,
                'value': int(value)
            }]
        flash('На складе больше нет такого товара')
    else:
        # добавляем товар к сессии в виде словаря
        # для этого в цикле ищем товар добавленный в сессию с таким же id
        # если к концу цикла не находим, то добавляем в сессию новый товар
        a = 0
        for elem in session['cart']:
            a += 1
            if int(elem['product_id']) == int(id):

                validation_value = quantity_validation(id_product, elem['value'], value)
                if validation_value:
                    session['cart'].remove(elem)
                    elem['value'] = elem['value'] + int(value)
                    if elem['value'] < 1:
                        del_in_cart(elem['product_id'], session)
                        return flash('На складе больше нет такого товара')
                    session['cart'].append(elem)
                    session.modified = True
                    break
                return flash('На складе больше нет такого товара')

            if a == len(session['cart']):
                validation_value = quantity_validation(id_product, 0, value)
                if validation_value:
                    session['cart'].append({
                        'product_id': id,
                        'value': int(value)
                    })
                    session.modified = True
                    break
                break
    in_cart = product_in_cart(session)
    cart_informations = cart_info(session)
    return render_template('cart.html', session=session, data=in_cart, cart_info=cart_informations)


def del_in_cart(product_id, session):
    a = 0
    for elem in session['cart']:
        if elem['product_id'] == product_id:
            del session['cart'][a]
        a += 1
    return session


@app.route('/<variable_name>/<path:subpath>', methods=['POST', 'GET'])
def categories_menu(variable_name, subpath):
    request_path = request
    if request.method == 'POST':
        try:
            do_in_cart(request.form['add_id'], session, int(request.form['number_of_additions']))
        except:
            do_in_cart(request.form['add_id'], session)
    if variable_name == 'product-card':
        display = product_card(subpath)
    elif variable_name == 'add-to-cart':
        do_in_cart(subpath, session)
        return redirect(url_for('cart'))
    else:
        display = redirect_for_subpath(subpath, request_path)
    return display


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/product-card/<path:subpath>')
def product_card(subpath):
    cart_informations = cart_info(session)
    items = Products.query.filter_by(id=str(subpath))
    return render_template('product_card.html', cart_info=cart_informations, product_info=items, product_card=[1, 2])


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


def transformation_in_int(value):
    if type(value) == int:
        return value
    elif value == "-":
        return 0
    elif " " in value:
        output_int = int(value.replace(' ', ''))
        return output_int
    elif ">" in value:
        output_int = int(value.replace(">", ''))
        return output_int



def product_in_cart(session):
    product_in_cart = []
    for elem in session['cart']:
        product_info = dict()
        items = Products.query.filter_by(id=str(elem['product_id']))
        product_info['price'] = transformation_in_int(items[0].price)
        product_info['title'] = items[0].title
        product_info['id'] = elem['product_id']
        product_info['value'] = int(elem['value'])
        product_info['producer'] = items[0].producer
        product_info['image'] = items[0].image
        product_info['balance'] = transformation_in_int(items[0].balance)
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
        if ('del_id' in request.form) or ('del_one_id' in request.form):
            if 'del_id' in request.form:
                product_id = request.form['del_id']
                del_in_cart(product_id, session)
            else:
                product_id = request.form['del_one_id']
                do_in_cart(product_id, session, -1)
            session.modified = True
            return redirect(url_for('cart'))
        elif 'add_one_id' in request.form:
            do_in_cart(request.form['add_one_id'], session)
            session.modified = True
            return redirect(url_for('cart'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()
        if user == None:
            flash('Пользователя с таким логином или паролем не существует')
            return redirect(url_for('login'))
        if check_password_hash(str(user.password), str(password)):
            login_user(user, remember=True)
            return redirect(url_for('profile'))
        else:
            flash('Пользователя с таким логином или паролем не существует')
            return redirect(url_for('login'))
    cart_informations = cart_info(session)
    return render_template('login.html', cart_info=cart_informations)


class UserHistory:
    def remove_characters(self, string):
        arr_orders = []
        for i in range(string.count(';')):
            arr_orders.append(string[0:string.find(';')])
            string = string[string.find(';') + 1:]
        return arr_orders


    def get_pending_order(self, email):
        order = HistorySells.query.filter_by(user_email=email).first()
        if len(order.last_order) > 0:
            arr_last_order = self.remove_characters(order.last_order)
            arr_items = []
            for elem in arr_last_order:
                items = Products.query.filter_by(id=int(elem)).first()
                arr_items.append(items)
            if order.order_status == 'Active':
                return arr_items
        else:
            return False


    @staticmethod
    def write_pending_order(self, email, arr_id_orders):
        pass


    @staticmethod
    def get_history_purchase(self, email):
        history_purchase = HistorySells.query.filter_by(user_email=email).first()


    @staticmethod
    def add_to_history(self, email, arr_id_orders):
        pass


@app.route('/profile')
@login_required
def profile():
    cart_informations = cart_info(session)
    email = current_user.email
    pending_order = UserHistory().get_pending_order(email)
    return render_template('profile.html', pending_order=pending_order, cart_info=cart_informations)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


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
    if len(phone) > 8:
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
                return render_template('success.html', cart_info=cart_informations)
            except:
                db.session.rollback()
                print('Error ad in db')
                return render_template('registration.html', cart_info=cart_informations)
        else:
            if validation['phone'] != True:
                flash(validation['phone'])
                return redirect(url_for('registration'))
            elif validation['email'] != True:
                flash(validation['email'])
                return redirect(url_for('registration'))
            else:
                flash('Введённые данные некорректны')
                return render_template('registration.html', cart_info=cart_informations)


if __name__ == "__main__":
    app.run(debug=True)
