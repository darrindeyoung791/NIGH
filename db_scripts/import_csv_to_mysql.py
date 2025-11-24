#!/usr/bin/env python3
"""
Script to import article data from CSV/text files to MySQL database
The script generates a UUID for each record and handles both CSV and text formats
"""

import os
import uuid
import mysql.connector
import pandas as pd
import glob
from pathlib import Path
import re
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_connection():
    """Create MySQL database connection"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),  # Use environment variable, default to 'localhost'
            user=os.getenv('DB_USER', 'nigh_content_user'),  # Use environment variable, default to 'nigh_content_user'
            password=os.getenv('DB_PASSWORD', 'nigh_secure_password'),  # Use environment variable, default to 'nigh_secure_password'
            database=os.getenv('DB_NAME', 'content_db')  # Use environment variable, default to 'content_db'
        )
        return conn
    except mysql.connector.Error as err:
        logger.error(f"Error connecting to MySQL: {err}")
        raise

def generate_uuid():
    """Generate a UUID string"""
    return str(uuid.uuid4())

def parse_file_content(file_path):
    """
    Parse content from file that follows the specified format:
    filename, url, time, language, title, content
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content by newlines to separate the metadata from the actual content
    lines = content.split('\n', 5)  # Split into at most 6 parts
    
    if len(lines) >= 6:
        filename, url, time_recorded, language, title = lines[:5]
        content = '\n'.join(lines[5:])  # The rest is the article content
    else:
        # If file doesn't follow the expected format, return basic info
        filename = Path(file_path).name
        url = ""
        time_recorded = ""
        language = ""
        title = ""
        content = '\n'.join(lines)
    
    return {
        'filename': filename.strip(),
        'url': url.strip(),
        'time_recorded': time_recorded.strip(),
        'language': language.strip(),
        'title': title.strip(),
        'content': content.strip()
    }

def import_csv_files_to_mysql(data_path):
    """Import CSV and text files to MySQL database"""
    conn = create_connection()
    cursor = conn.cursor()
    
    # Find all CSV and text files in the specified directory
    csv_files = glob.glob(os.path.join(data_path, "*.csv"))
    txt_files = glob.glob(os.path.join(data_path, "*.txt"))
    all_files = csv_files + txt_files
    
    if not all_files:
        logger.warning(f"No CSV or TXT files found in {data_path}")
        return
    
    logger.info(f"Found {len(all_files)} files to process")
    
    # Count processed files
    processed_count = 0
    
    for file_path in all_files:
        logger.info(f"Processing file: {file_path}")
        
        try:
            # Check if it's a CSV file
            if file_path.lower().endswith('.csv'):
                # Read CSV file
                df = pd.read_csv(file_path)
                
                # Assuming column order: filename, url, time, language, title, content
                # If column names are different, adjust accordingly
                if list(df.columns) == ['filename', 'url', 'time', 'language', 'title', 'content']:
                    df = df.rename(columns={
                        'filename': 'filename',
                        'url': 'url',
                        'time': 'time_recorded',
                        'language': 'language',
                        'title': 'title',
                        'content': 'content'
                    })
                elif len(df.columns) == 6:
                    # If columns don't have proper names, assign them
                    df.columns = ['filename', 'url', 'time_recorded', 'language', 'title', 'content']
                
            elif file_path.lower().endswith('.txt'):
                # Handle text file with specified format
                parsed_data = parse_file_content(file_path)
                df = pd.DataFrame([parsed_data])
            
            else:
                logger.warning(f"Skipping unsupported file: {file_path}")
                continue
            
            # Insert each row into the database
            for index, row in df.iterrows():
                record_id = generate_uuid()
                
                # Prepare data for insertion
                filename = row.get('filename', '')
                url = row.get('url', '')
                time_recorded = row.get('time_recorded', '')
                language = row.get('language', '')
                title = row.get('title', '')
                content = row.get('content', '')
                
                # Insert into database
                query = """
                INSERT INTO articles (id, filename, url, time_recorded, language, title, content)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(query, (record_id, filename, url, time_recorded, language, title, content))
            
            conn.commit()
            processed_count += 1
            logger.info(f"Successfully processed {file_path}")
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            conn.rollback()
    
    cursor.close()
    conn.close()
    
    logger.info(f"Import completed. Processed {processed_count} files successfully.")

def main():
    # Get the path to import from as argument or use default
    import sys
    
    if len(sys.argv) > 1:
        data_path = sys.argv[1]
    else:
        # Default path where the raw data is stored
        data_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'raw data')
    
    # Normalize path
    data_path = os.path.abspath(data_path)
    
    if not os.path.exists(data_path):
        logger.error(f"Data path does not exist: {data_path}")
        return
    
    logger.info(f"Importing files from: {data_path}")
    import_csv_files_to_mysql(data_path)

if __name__ == "__main__":
    main()