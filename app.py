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


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    firstname = bleach.clean(html.escape(request.form.get('firstname', '')).strip(), tags=allowed_tags,
                             attributes=allowed_attributes)
    lastname = bleach.clean(html.escape(request.form.get('lastname', '')).strip(), tags=allowed_tags,
                            attributes=allowed_attributes)
    email = bleach.clean(html.escape(request.form.get('email', '')).strip(), tags=allowed_tags,
                         attributes=allowed_attributes)
    country = bleach.clean(html.escape(request.form.get('country', '')).strip(), tags=allowed_tags,
                           attributes=allowed_attributes)
    message = bleach.clean(html.escape(request.form.get('message', '')).strip(), tags=allowed_tags,
                           attributes=allowed_attributes)
    gender = bleach.clean(html.escape(request.form.get('gender', '')).strip(), tags=allowed_tags,
                          attributes=allowed_attributes)
    subjects = [bleach.clean(subject, tags=allowed_tags, attributes=allowed_attributes) for subject in
                request.form.getlist('subjects')]
    honeypot = bleach.clean(html.escape(request.form.get('honeypot', '')).strip(), tags=allowed_tags,
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
    if honeypot:
        return redirect(url_for('index'))  # Si le honeypot est rempli, rediriger sans action

    if errors:
        for field, error in errors.items():
            flash(error, field)
        return render_template('form.html', firstname=firstname, lastname=lastname, email=email, country=country,
                               message=message, gender=gender, subjects=subjects)

    # Prepare datas for the SQL insertion
    gender = 1 if gender == 'H' else 0
    country = country[0:2]

    db.insert_data(gender, firstname, lastname, email, message, subjects, country)

    return render_template('show.html', firstname=firstname, lastname=lastname, email=email, country=country,
                           message=message, gender=gender, subjects=subjects)


@app.route('/list', methods=['GET'])
def fetch_all():
    results = db.fetch_all()

    return render_template('list.html', users=results)


@app.route('/list/<id>', methods=['GET'])
def list_one_by(id):
    result = db.fetch_one_by(id)

    return render_template('profile.html', user=result)

@app.route('/list/delete', methods=['POST'])
def delete_one_by():

    id = int(bleach.clean(html.escape(request.form.get('user_id', ''))))
    db.delete_one_by(id)

    results = db.fetch_all()
    return render_template('list.html', users=results)


if __name__ == '__main__':
    app.run(debug=True)
