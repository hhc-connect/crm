from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import add_customer, list_customers, search_customers, delete_customer, update_customer_status

app = Flask(__name__)
app.secret_key = '73583835'

@app.route('/')
def index():
    if 'logged_in' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'HHC' and password == 'Kirche123#1':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Login fehlgeschlagen!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer_route():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        note = request.form['note']
        add_customer(name, email, phone, address, note)
        flash('Kunde erfolgreich hinzugefügt.', 'success')
        return redirect(url_for('customers_route'))
    return render_template('add_customer.html')

@app.route('/customers')
def customers_route():
    customers = list_customers()
    return render_template('customers.html', customers=customers)

@app.route('/search_customers', methods=['GET', 'POST'])
def search_customers_route():
    if request.method == 'POST':
        name = request.form['search_name']
        email = request.form['search_email']
        phone = request.form['search_phone']
        address = request.form['search_address']
        status = request.form['search_status']
        customers = search_customers(name, email, phone, address, status)
        return render_template('customers.html', customers=customers)
    return render_template('search_customer.html')

@app.route('/update_status', methods=['GET', 'POST'])
def update_status_route():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        new_status = request.form['new_status']
        update_customer_status(customer_id, new_status)
        flash('Kundenstatus aktualisiert.', 'info')
        return redirect(url_for('customers_route'))
    return render_template('update_status.html')

@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer_route(customer_id):
    delete_customer(customer_id)
    flash('Kunde gelöscht.', 'warning')
    return redirect(url_for('customers_route'))

if __name__ == '__main__':
    app.run(debug=True)
