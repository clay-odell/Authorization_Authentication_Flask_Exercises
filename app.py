from flask import Flask, render_template, redirect, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegistrationForm, LoginForm, FeedbackForm
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
        session['user_id'] = new_user.id        
        return redirect(f"/users/{new_user.username}")
    else:
               
        return render_template('user_register.html', form=form)
        
@app.route('/users/<username>')
def user_profile_view(username):
    """User Profile View"""
    user = User.query.filter_by(username=username).first()
    feedback = Feedback.query.filter_by(username=username).all()
    if "user_id" not in session:
        flash("Please login first!")
        return redirect('/login')
    
    return render_template('user_profile.html', user=user, feedback=feedback)

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    """Login User Accepts Username & Password"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!")
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.password.errors.append('Invalid username/password')
    return render_template('login_form.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout_user():
    if 'user_id' in session:
        session.clear()
        return redirect('/login')
    else:
        flash("You are not currently logged in.")
        return redirect('/login')
    
    
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user_post(username):
    """Delete User from Database POST route"""
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash("Your account has been deleted.", "success")
        return redirect('/register')
    else:
        flash("User not found.", "danger")
        return redirect('/register')

@app.route('/users/<username>/delete', methods=['GET'])
def delete_user_get(username):
    """Delete User GET Route"""
         
    user = User.query.filter_by(username=username).first()
    if 'username' not in session:
        flash("You must be logged in to delete account.", "danger")
        return redirect('/login')
    elif session['username'] != username:
        flash("You can only delete your own account.")
        return redirect(f'/users/{user.username}')
    return render_template('delete_user.html', user=user)

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_user_feedback(username):
    """Add User Feedback"""
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.", "danger")
        return redirect('login')
    elif 'username' not in session or session['username'] != username:
        flash("You must be logged in to post feedback.", "danger")
        return redirect('/login')
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        flash("Your feedback has been posted.", "success")
        return redirect(f'/users/{user.username}')
    return render_template('feedback_form.html', form=form, user=user)
    
@app.route('/feedback/<feedback_id>/update', methods=['GET'])
def update_feedback_get(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    user = Feedback.query.filter_by(username=feedback.username).first()
    form = FeedbackForm()
    return render_template('edit_feedback.html', feedback=feedback, form=form, user=user)

@app.route('/feedback/<feedback_id>/update', methods=['POST'])
def update_feedback_patch(feedback_id):
   feedback = Feedback.query.get(feedback_id)
   form = FeedbackForm()
   if form.validate_on_submit():
       feedback.title = form.title.data
       feedback.content = form.content.data
       db.session.commit()
       return redirect(f'/users/{feedback.username}')
        
    
        
        
    