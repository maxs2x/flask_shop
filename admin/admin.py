from flask import Blueprint, render_template, request, url_for, redirect, flash, session



admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

def login_admin():
    session['admin_logget'] = 1


def isLogget():
    return True if session.get('admin_logget') else False


def logout_admin():
    session.pop('admin_logget', None)


@admin.route('/')
def index():
    if not isLogget():
        return redirect(url_for('.login'))
    return render_template('admin/index.html')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if isLogget():
        return redirect(url_for('.index'))
    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['password'] == 'peppa':
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash('Неверная пара логин-пароль', 'error')
    return render_template('admin/login.html', title='Админ-панель')


@admin.route('/logout')
def logout():
    if not isLogget():
        return redirect(url_for('.login'))
    logout_admin()
    return redirect(url_for('.login'))


@admin.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        balance = request.form['balance']
        description = request.form['description']
        producer = request.form['producer']
        model_auto = request.form['model_auto']
        navigation_categories = request.form['navigation_categories']
        image = request.form['image']
        image_alt = request.form['image_alt']

        item = Products(title=title, price=price, balance=balance, description=description, producer=producer,
                        model_auto=model_auto, navigation_categories=navigation_categories, image=image, image_alt=image_alt)

        try:
            db.session.add(item)
            db.session.commit()
            return render_template('index.html')
        except:
            return "Error in db"
    else:
        return render_template('admin/create.html')




#<div class="col d-none d-lg-block bg-warning bg-gradient  ">