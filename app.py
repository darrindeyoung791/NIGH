from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
# Check if MySQL environment variables are set, otherwise use SQLite
if os.getenv('DB_HOST'):
    # Use MySQL database configuration from environment variables
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'nigh_content_user')
    db_password = os.getenv('DB_PASSWORD', 'nigh_secure_password')
    db_name = os.getenv('DB_NAME', 'content_db')
    # Using PyMySQL for Flask-SQLAlchemy (as it's more commonly used with SQLAlchemy)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
else:
    # Fallback to SQLite if MySQL environment variables are not set
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)