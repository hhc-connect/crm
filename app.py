from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from database import add_customer, list_customers, delete_customer, update_customer_status, search_customers_by_query, export_customers_to_csv
from flask import send_file

app = Flask(__name__)

users = {'HHC': {'password': 'Kirche123#1'}}

app.secret_key = os.environ.get('SECRET_KEY', 'Ein_default_geheimer_Schlüssel')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user_obj = User()
            user_obj.id = username
            login_user(user_obj)
            return redirect(url_for('index'))
        return 'Ungültige Anmeldedaten'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer_route():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        note = request.form['note']
        add_customer(name, email, phone, address, note)
        return redirect(url_for('list_customers_route'))
    return render_template('add_customer.html')

@app.route('/customers')
def list_customers_route():
    customers = list_customers()
    return render_template('list_customers.html', customers=customers)

@app.route('/search_customers_by_query', methods=['GET', 'POST'])
def search_customers_route():
    if request.method == 'POST':
        search_name = request.form.get('search_name')
        search_email = request.form.get('search_email')
        search_phone = request.form.get('search_phone')
        search_address = request.form.get('search_address')
        search_status = request.form.get('search_status')

        results = search_customers_by_query(search_name, search_email, search_phone, search_address, search_status)
        return render_template('list_customers.html', customers=results)
    return render_template('search_customers.html')


@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer_route(customer_id):
    delete_customer(customer_id)
    return redirect(url_for('list_customers_route'))

@app.route('/update_status', methods=['GET', 'POST'])
def update_status_route():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        new_status = request.form.get('new_status')
        if customer_id and new_status:
            update_customer_status(customer_id, new_status)
            return redirect(url_for('list_customers_route'))
    return render_template('update_status.html')

@app.route('/export_customers')
def export_customers_route():
    export_customers_to_csv('customers.csv')  # Funktion, die die CSV-Datei erstellt
    return send_file('customers.csv', as_attachment=True, attachment_filename='customers.csv')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
