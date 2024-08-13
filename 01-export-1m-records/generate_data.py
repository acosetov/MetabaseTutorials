import os
import sys
import psycopg2
from faker import Faker
from psycopg2.extras import execute_batch
from multiprocessing import Pool

fake = Faker()

def generate_data_chunk(chunk_size):
    data = []
    for _ in range(chunk_size):
        data.append((
            fake.name(),
            fake.email(),
            fake.date_of_birth(minimum_age=18, maximum_age=90),
            fake.country(),
            fake.random_int(min=1000, max=100000)
        ))
    return data

def insert_data(chunk_data):
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('PGDATABASE', 'generated_data'),
            user=os.environ.get('PGUSER', 'data_user'),
            password=os.environ.get('PGPASSWORD', 'data_password'),
            host=os.environ.get('PGHOST', 'postgres')
        )
        cur = conn.cursor()
        
        execute_batch(cur, """
        INSERT INTO users (name, email, birth_date, country, salary)
        VALUES (%s, %s, %s, %s, %s)
        """, chunk_data, page_size=10000)
        
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred during insertion: {e}")
        sys.exit(1)

def main():
    print("Starting data generation and insertion script...")
    
    # Database connection for table creation
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('PGDATABASE', 'generated_data'),
            user=os.environ.get('PGUSER', 'data_user'),
            password=os.environ.get('PGPASSWORD', 'data_password'),
            host=os.environ.get('PGHOST', 'postgres')
        )
        cur = conn.cursor()
        
        print("Creating users table...")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            birth_date DATE,
            country VARCHAR(100),
            salary INTEGER
        )
        """)
        conn.commit()
        print("Users table created or already exists.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred during table creation: {e}")
        sys.exit(1)

    # Parallel processing for data generation and insertion
    num_records = 1200000
    num_workers = 8  # Adjust based on your CPU cores
    chunk_size = num_records // num_workers

    print(f"Generating and inserting {num_records} records using {num_workers} workers...")

    with Pool(num_workers) as pool:
        data_chunks = [pool.apply_async(generate_data_chunk, (chunk_size,)) for _ in range(num_workers)]
        for chunk in data_chunks:
            insert_data(chunk.get())

    print("Data insertion completed.")

if __name__ == "__main__":
    main()