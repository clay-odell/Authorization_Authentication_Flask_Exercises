from flask import Flask, render_template, redirect, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegistrationForm, LoginForm
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01302@localhost/users_demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'my-super-secret-key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def redirect_to_register():
    """Returns to Register Route"""
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def user_register():
    """Register User View"""
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()        
        return redirect('/secret')
    else:
        return render_template('user_register.html', form=form)
        
@app.route('/secret')
def secrethome():
    """Renders Secret.html"""
    return render_template('secret.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    """Login User Accepts Username & Password"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        check_user = User.authenticate(username, password)
        if check_user:
            return render_template('secret.html')
        else:
            return redirect('/register')
    else:
        return render_template('login_form.html', form=form)
                