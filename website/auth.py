from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    email = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Ingresaste a la cuenta!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Contrasena incorrecta, intenta de nuevo.', category='error')
        else:
            flash('El correo no existe, crea una cuenta para ingresar', category='error')

    return render_template("login.html", email=email, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('El correo ya esta en uso', category='error')
        elif len(email) < 4:
            flash('El correo debe tener al menos 4 caracteres', category='error')
        elif len(first_name) < 2:
            flash('El nombre debe tener al menos 2 caracteres', category='error')
        elif password1 != password2:
            flash('Las contrsenas no son iguales', category='error')
        elif len(password1) < 7:
            flash('La contrasena debe contener al menos 7 caracteres', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Cuenta creada!', category='success')
            return redirect(url_for('views.home'))


    return render_template("sign_up.html", user=current_user)