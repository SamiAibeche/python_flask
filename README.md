# Flask Contact Form Application

This project is a simple Flask web application that includes a contact form. The form includes fields for first name, last name, email, country, message, gender, and subjects of interest. The application sanitizes inputs to prevent XSS attacks and stores form submissions in a MySQL database.

## Features

- Contact form with input sanitization
- Error handling with flash messages
- Form validation
- SQL Injection protection
- Custom 404 error page
- Secure session management

## Requirements

- Python 3.x
- Flask
- MySQL
- `python-dotenv`
- `mysql-connector-python`
- `bleach`

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/SamiAibeche/python_flask.git
    cd python_flask
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up your environment variables**:
    Create a `.env` file in the root directory of the project and add the following variables:
    ```env
    FLASK_SECRET_KEY=your_secret_key
    DB_HOST=your_db_host
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=your_db_name
    ```

5. **Set up your MySQL database**:
    Ensure you have a MySQL database set up and configured according to the environment variables in your `.env` file.

## Usage

1. **Run the Flask application**:
    ```sh
    flask run
    ```
    The application will start and be accessible at `http://127.0.0.1:5000`.

## File Structure

````pycon
python_flask/
├── app.py # Main application file
├── Databases.py # Database operations
├── requirements.txt # Python dependencies
├── .env # Environment variables
├── templates/
│ ├── form.html # Contact form template
│ ├── success.html # Success page template
│ ├── 404.html # Custom 404 error page template
└── README.md # This file
````