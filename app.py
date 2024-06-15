from flask import Flask, render_template, request, redirect, url_for, flash
import re
import html
import bleach
import os
from dotenv import load_dotenv
from Database import Database

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

allowed_tags = ['b', 'i', 'u', 'strong', 'em']
allowed_attributes = {
    '*': ['class', 'style']
}

db = Database()  # Create an instance of the Database class


def sanitize(input):
    return bleach.clean(html.escape(input).strip(), tags=allowed_tags, attributes=allowed_attributes)


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    # Input Sanitization
    firstname = sanitize(request.form.get('firstname', ''))
    lastname = sanitize(request.form.get('lastname', ''))
    email = sanitize(request.form.get('email', ''))
    country = sanitize(request.form.get('country', ''))
    message = sanitize(request.form.get('message', ''))
    gender = sanitize(request.form.get('gender', ''))

    subjects = [bleach.clean(subject, tags=allowed_tags, attributes=allowed_attributes) for subject in
                request.form.getlist('subjects')]
    error_msg = bleach.clean(html.escape(request.form.get('error_msg', '')).strip(), tags=allowed_tags,
                            attributes=allowed_attributes)
    countries = ['France', 'Belgium', 'Canada', 'Switzerland']

    if subjects and len(subjects) >= 1:
        subjects = ",".join(subjects)
    else:
        subjects = ("")

    errors = {}
    if not firstname:
        errors['firstname'] = 'First name is required.'
    if not lastname:
        errors['lastname'] = 'Last name is required.'
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors['email'] = 'Valid email is required.'
    if country not in countries:
        errors['country'] = 'Valid country is required.'
    if not message:
        errors['message'] = 'Message is required.'
    if gender not in ['H', 'F']:
        errors['gender'] = 'Gender is required.'
    if error_msg:
        return redirect(url_for('index'))  # If errors have been found

    # Flash errors management
    if errors:
        for field, error in errors.items():
            flash(error, field)
        return render_template('form.html', firstname=firstname, lastname=lastname, email=email, country=country,
                               message=message, gender=gender, subjects=subjects)

    # Prepare datas for the SQL insertion
    gender = 1 if gender == 'H' else 0
    country = country[0:2]

    db.insert_datas(gender, firstname, lastname, email, message, subjects, country)

    return render_template('show.html', firstname=firstname, lastname=lastname, email=email, country=country,
                           message=message, gender=gender, subjects=subjects)


@app.route('/list', methods=['GET'])
def fetch_all():
    results = db.fetch_all()

    return render_template('list.html', users=results)


@app.route('/list/<id>', methods=['GET'])
def list_one_by(id):
    result = db.fetch_one_by(id)
    if result is None:
        return render_template('404.html')
    else:
        return render_template('profile.html', user=result)


@app.route('/list/delete', methods=['POST'])
def delete_one_by():
    id = int(sanitize(request.form.get('user_id', '')))
    db.delete_one_by(id)

    results = db.fetch_all()
    msg = "User " + str(id) + " has been deleted"

    flash(msg)  # Flash usage
    return render_template('list.html', users=results)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
