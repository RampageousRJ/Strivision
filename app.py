from flask import Flask, render_template, request, redirect, url_for,flash, session, g
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from striver import get_login_token, fetch_user_data, get_user_stats, unstar_question
from potd import get_leetcode_daily_challenge, get_gfg_daily_challenge
import re
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login', render_kw={"class": "btn btn-primary"})

def validEmail(email_text):
    if re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',email_text) is not None:
        return True
    return False

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    if hasattr(g, 'start_time'):
        elapsed_time = time.time() - g.start_time
        # You can log this time or add it to the response headers
        print(f"Request to {request.path} took {elapsed_time:.4f} seconds")
        # Example: Add to response headers
        response.headers["X-Page-Load-Time"] = f"{elapsed_time:.4f}s"
    return response

@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            token, username = get_login_token(email, password)
            session['token'] = token
            session['username'] = username
            session['email'] = email
        except Exception as e:
            print(f"Error during login: {e}")
            flash('Invalid email or password. Please try again or visit <a href="https://takeuforward.org/login" style="text-decoration:none;">this website</a> to generate credentials.', 'danger')
            return redirect(url_for('home') + '#login')
        return redirect(url_for('dashboard'))
    return render_template('home.html', form = form)

@app.route('/dashboard')
def dashboard():
    if 'token' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('home'))
    
    token = session['token']
    username = session['username']
    email = session['email']
    
    try:
        leetcode_link = get_leetcode_daily_challenge()
        gfg_link = get_gfg_daily_challenge()
        user_stats = get_user_stats(username, token)
        user_data = fetch_user_data(email, token)
        if not leetcode_link or not gfg_link:
            print('Could not fetch daily challenges. Please try again later.', 'warning')
    except Exception as e:
        print(f"Error fetching data: {e}")
        flash(f'Error fetching data: {str(e)}', 'danger')
        return redirect(url_for('home'))

    return render_template('dashboard.html', username=username, leetcode_link=leetcode_link, gfg_link=gfg_link, user_stats=user_stats, user_data=user_data)

@app.route('/unstar', methods=['POST'])
def unstar():
    if 'token' not in session or 'email' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('home'))
    
    token = session['token']
    email = session['email']
    question_id = request.form.get('question_id')
    try:
        success = unstar_question(token, email, question_id)
        if success:
            print(f'Question {question_id} has been successfully unstared.', 'success')
        else:
            print(f'Failed to unstar question {question_id}.', 'danger')
    except Exception as e:
        print(f"Error unstarring question {question_id}: {e}")
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('token', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)