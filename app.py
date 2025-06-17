from flask import Flask, render_template, request, redirect, url_for,flash, session
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from striver import get_login_token, get_entire_sheet, get_starred_questions, fetch_user_data, get_user_stats
from potd import get_leetcode_daily_challenge, get_gfg_daily_challenge, get_hackerearth_daily_challenge
import re

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
            get_entire_sheet(email, token)
            get_starred_questions(email, token)
            fetch_user_data()

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
        hackerearth_link = get_hackerearth_daily_challenge()
        user_stats = get_user_stats(username, token)
        if not leetcode_link or not gfg_link:
            flash('Could not fetch daily challenges. Please try again later.', 'warning')
            leetcode_link = gfg_link = None
    except Exception as e:
        flash(f'Error fetching data: {str(e)}', 'danger')
        return redirect(url_for('home'))

    return render_template('dashboard.html', username=username, leetcode_link=leetcode_link, gfg_link=gfg_link, user_stats=user_stats, hackerearth_link=hackerearth_link)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)