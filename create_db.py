import psycopg2

conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname='car_rental_db',
        user='user',
        password='password')
conn.autocommit = True
# Open a cursor to perform database operations
cur = conn.cursor()
INSERT INTO user_model (login, password, is_admin) VALUES ('admin', 'admin', True);
INSERT INTO user_model (login, password, is_admin) VALUES ('admin', 'admin', True);
INSERT INTO user_model (login, password, is_admin) VALUES ('admin', 'admin', True);
INSERT INTO user_model (login, password, is_admin) VALUES ('admin', 'admin', True);
INSERT INTO user_model (login, password, is_admin) VALUES ('admin', 'admin', True);


# Execute a command: this creates a new table
# cur.execute('CREATE DATABASE car_rental_db;')
# cur.execute('CREATE TABLE Cars (id SERIAL NOT NULL,brand VARCHAR(150) NOT NULL,version INT NOT NULL,year INT NOT NULL,PRIMARY KEY (id));')
# cur.execute('CREATE TABLE Users (id SERIAL NOT NULL,login VARCHAR(150) UNIQUE NOT NULL,password VARCHAR(150) NOT NULL,is_admin BOOLEAN NOT NULL,PRIMARY KEY (id));')
# cur.execute('CREATE TABLE Reservations (id SERIAL NOT NULL,date_from DATE NOT NULL,date_to DATE NOT NULL,car_id int,FOREIGN KEY (car_id) REFERENCES Cars(id),PRIMARY KEY (id));')

# # Insert data into the table

# cur.execute('INSERT INTO Users (login, password, is_admin)'
#             'VALUES (%s, %s, %s)',
#             ('user',
#              'password',
#              False)
#             )

# cur.execute('INSERT INTO Users (login, password, is_admin)'
#             'VALUES (%s, %s, %s)',
#             ('admin',
#              'admin',
#              True)
#             )

# cur.execute('INSERT INTO Cars (brand, version, year)'
#             'VALUES (%s, %s, %s)',
#             ('toyota',
#              2,
#              2005)
#             )

# cur.execute('INSERT INTO Reservations (date_from, date_to, car_id)'
#             'VALUES (%s, %s, %s)',
#             ('2022-06-01',
#              '2022-06-04',
#              1)
#             )

conn.commit()

cur.close()
conn.close()