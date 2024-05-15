### Data Pipeline Ticketing Project

#### Overview
This repository houses the code leveraged for a mini-project to ingest delimited flat files from first principles. An example <tt>.csv</tt> file was provided to test the ingestion pipeline, with an example query performed at the end to verify results.

#### Folder Structure
The elements of this project are divided into the following directories:

- <tt>data</tt>: The source code expects the flat file for ingestion to be stored in this folder

- <tt>logs</tt>: Stores application logs during running of the program

- <tt>src</tt>: Contains Python files that manage all functions and the command line application

#### How to Use
To run this program using Python, the user must provide the following:

1) An installation of MySQL https://www.mysql.com/ and the assocated connector for Python, which can be obtained via PIP:

```sh
pip3 install mysql-connector-python
```

2) A comma-delimited text file without headers stored in the <tt>data</tt> folder using the following schema:

```sh
            ticket_id INT,
            trans_date INT,
            event_id INT,
            event_name VARCHAR(50),
            event_date DATE,
            event_type VARCHAR(10),
            event_city VARCHAR(20),
            customer_id INT,
            price DECIMAL(10,2),
            num_tickets INT
```

3) Creation of a <tt>.env</tt> file in the following format to store sensitive variables:

```sh
DB_USER="..."
DB_PASSWORD="..."
HOST="..."
PORT=".."
```

From the terminal, navigate to the <tt>src</tt> directory and run the following:

```sh
python app.py
```

The output should be the same as that shown <a href="https://github.com/andrewcockerill/springboard_07_data_pipeline/blob/main/src/app_run.txt">here</a>.