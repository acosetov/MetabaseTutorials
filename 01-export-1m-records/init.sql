-- Create Metabase database and user
CREATE DATABASE metabase;
CREATE USER metabase WITH PASSWORD 'metabase_password';
GRANT ALL PRIVILEGES ON DATABASE metabase TO metabase;

-- Connect to the metabase database
\c metabase

-- Grant necessary permissions to metabase user
GRANT ALL PRIVILEGES ON SCHEMA public TO metabase;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO metabase;

-- Create database for generated data
CREATE DATABASE generated_data;
CREATE USER data_user WITH PASSWORD 'data_password';
GRANT ALL PRIVILEGES ON DATABASE generated_data TO data_user;

-- Connect to the generated_data database
\c generated_data

-- Grant necessary permissions to data_user
GRANT ALL PRIVILEGES ON SCHEMA public TO data_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO data_user;