import sqlite3
import os
import csv

def get_db_connection():
    db_path = os.environ.get('DATABASE_PATH', 'crm.db')
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_db():
    connection = get_db_connection()
    with connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                note TEXT,
                purchase_status TEXT DEFAULT 'Rot'
            );
        """)
    connection.close()

def add_customer(name, email, phone, address, note):
    connection = get_db_connection()
    with connection:
        connection.execute("""
            INSERT INTO customers (name, email, phone, address, note, purchase_status) 
            VALUES (?, ?, ?, ?, ?, 'Gelb');""", 
            (name, email, phone, address, note))
    connection.close()

def list_customers():
    connection = get_db_connection()
    customers = connection.execute("SELECT * FROM customers;").fetchall()
    connection.close()
    return customers

def search_customers(name=None, email=None, phone=None, address=None, status=None):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM customers WHERE"
    parameters = []

    if name:
        query += " name LIKE ? AND"
        parameters.append('%' + name + '%')
    if email:
        query += " email LIKE ? AND"
        parameters.append('%' + email + '%')
    if phone:
        query += " phone LIKE ? AND"
        parameters.append('%' + phone + '%')
    if address:
        query += " address LIKE ? AND"
        parameters.append('%' + address + '%')
    if status:
        query += " purchase_status = ? AND"
        parameters.append(status)

    query = query.rstrip(' AND')

    cursor.execute(query, parameters)
    results = cursor.fetchall()
    connection.close()
    return results


def delete_customer(customer_id):
    connection = get_db_connection()
    with connection:
        connection.execute("DELETE FROM customers WHERE id = ?;", (customer_id,))
    connection.close()

def update_customer_status(customer_id, new_status):
    connection = get_db_connection()
    with connection:
        connection.execute("UPDATE customers SET purchase_status = ? WHERE id = ?;", (new_status, customer_id))
    connection.close()

def export_customers_to_csv(filename='customers.csv'):
    customers = list_customers()
    headers = ['ID', 'Name', 'Email', 'Telefon', 'Adresse', 'Notiz', 'Kaufstatus']

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for customer in customers:
            writer.writerow([customer['id'], customer['name'], customer['email'], customer['phone'], customer['address'], customer['note'], customer['purchase_status']])

def import_customers_from_csv(filename='customers.csv'):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            add_customer(name=row[1], email=row[2], phone=row[3], address=row[4], note=row[5])
