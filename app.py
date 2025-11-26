from flask import Flask, render_template, request
from flask import jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import the database instance and models after loading environment
from models import db, Article

app = Flask(__name__)

# Database configuration
# Using the exact MySQL configuration you specified with PyMySQL driver
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://nigh_content_user:nigh_secure_password@localhost/nigh_content_db'

# Check if MySQL environment variables are set, otherwise use SQLite
# if os.getenv('DB_HOST'):
#     # Use MySQL database configuration from environment variables
#     db_host = os.getenv('DB_HOST', 'localhost')
#     db_user = os.getenv('DB_USER', 'nigh_content_user')
#     db_password = os.getenv('DB_PASSWORD', 'nigh_secure_password')
#     db_name = os.getenv('DB_NAME', 'nigh_content_db')
#     # Using PyMySQL for Flask-SQLAlchemy (as it's more commonly used with SQLAlchemy)
#     app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
# else:
#     # Fallback to SQLite if MySQL environment variables are not set
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('main_dash.html')

@app.route('/search')
def search():
    """Search endpoint that will allow searching articles"""
    query = request.args.get('q', '')
    if query:
        # Search in the articles table
        articles = Article.query.filter(
            Article.title.contains(query) | Article.content.contains(query)
        ).all()
        results = [article.to_dict() for article in articles]
    else:
        results = []
    return jsonify(results)


@app.route('/article/<string:article_id>')
def article_detail(article_id):
    """Display a single article by its ID"""
    article = Article.query.filter_by(id=article_id).first_or_404()
    return render_template('article_detail.html', article=article)

if __name__ == '__main__':
    app.run(debug=True)