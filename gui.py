import csv
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from database import add_customer, list_customers, search_customers, update_customer_statuses, export_customers_to_csv, import_customers_from_csv, get_db_connection

def gui_add_customer():
    name = simpledialog.askstring("Neuer Kunde", "Name:")
    email = simpledialog.askstring("Neuer Kunde", "E-Mail:")
    phone = simpledialog.askstring("Neuer Kunde", "Telefon:")
    address = simpledialog.askstring("Neuer Kunde", "Adresse:")
    note = simpledialog.askstring("Neuer Kunde", "Notiz:")

    if name and email:
        add_customer(name, email, phone, address, note)
        messagebox.showinfo("Erfolg", "Kunde erfolgreich hinzugefügt.")
    else:
        messagebox.showerror("Fehler", "Name und E-Mail sind erforderlich.")

def gui_search_customers():
    name = simpledialog.askstring("Kunden suchen", "Name (optional):")
    email = simpledialog.askstring("Kunden suchen", "E-Mail (optional):")
    phone = simpledialog.askstring("Kunden suchen", "Telefon (optional):")
    address = simpledialog.askstring("Kunden suchen", "Adresse (optional):")

    results_window = tk.Toplevel()
    results_window.title("Suchergebnisse")

    tree = ttk.Treeview(results_window, columns=('ID', 'Name', 'Email', 'Telefon', 'Adresse', 'Notiz'), show='headings')
    for col in tree['columns']:
        tree.heading(col, text=col)
    tree.pack(expand=True, fill='both')

    results = search_customers(name, email, phone, address)
    for customer in results:
        tree.insert('', tk.END, values=(customer['id'], customer['name'], customer['email'], customer['phone'], customer['address'], customer['note']))

def gui_show_all_customers():
    customers_window = tk.Toplevel()
    customers_window.title("Alle Kunden")

    tree = ttk.Treeview(customers_window, columns=('ID', 'Name', 'Email', 'Telefon', 'Adresse', 'Notiz', 'Status'), show='headings')
    for col in tree['columns']:
        tree.heading(col, text=col)
    tree.pack(expand=True, fill='both')

    customers = list_customers()
    for customer in customers:
        color_tag = 'normal'  
        if customer['purchase_status'] == 'Grün':
            color_tag = 'green'
        elif customer['purchase_status'] == 'Gelb':
            color_tag = 'yellow'
        elif customer['purchase_status'] == 'Rot':
            color_tag = 'red'

        tree.insert('', tk.END, values=(customer['id'], customer['name'], customer['email'], customer['phone'], customer['address'], customer['note'], customer['purchase_status']), tags=(color_tag,))
        tree.tag_configure('green', background='lightgreen')
        tree.tag_configure('yellow', background='yellow')
        tree.tag_configure('red', background='salmon')

def export_customers_to_csv(filename='customers.csv'):
    customers = list_customers()
    headers = ['Adresse', 'Name', 'Telefonnummer', 'Uhrzeit', 'Notiz']

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for customer in customers:
           
            writer.writerow([customer['address'], customer['name'], customer['phone'], '', customer['note']])

import csv
from tkinter import messagebox
from database import add_customer

def import_customers_from_csv(filename='customers.csv'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) 
            for row in reader:
                add_customer(name=row[1], email='', phone=row[2], address=row[0], note=row[4])

        messagebox.showinfo("Information", "Import abgeschlossen")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")
def delete_customer(customer_id):
    connection = get_db_connection()
    with connection:
        connection.execute("DELETE FROM customers WHERE id = ?;", (customer_id,))
    connection.close()

def gui_delete_customer():
    customer_id = simpledialog.askstring("Kunden löschen", "Kunden-ID:")
    if customer_id:
        delete_customer(customer_id)
        messagebox.showinfo("Erfolg", f"Kunde mit ID {customer_id} wurde gelöscht.")
    else:
        messagebox.showerror("Fehler", "Kunden-ID ist erforderlich.")

def main():
    window = tk.Tk()
    window.title("CRM-System")
    window.geometry("800x600")  
    window.configure(bg='gray') 

    button_style = {'font': ('Helvetica', 12), 'padx': 10, 'pady': 10, 'bg': 'white', 'fg': 'black'}

    add_customer_button = tk.Button(window, text="Neuen Kunden anlegen", command=gui_add_customer, **button_style)
    add_customer_button.pack(pady=(10, 0))

    search_customers_button = tk.Button(window, text="Kunden suchen", command=gui_search_customers, **button_style)
    search_customers_button.pack(pady=(10, 0))

    show_all_customers_button = tk.Button(window, text="Alle Kunden anzeigen", command=gui_show_all_customers, **button_style)
    show_all_customers_button.pack(pady=(10, 0))

    update_status_button = tk.Button(window, text="Kundenstatus aktualisieren", command=update_customer_statuses, **button_style)
    update_status_button.pack(pady=(10, 10))
    
    delete_customer_button = tk.Button(window, text="Kunden löschen", command=gui_delete_customer)
    delete_customer_button.pack()

    export_button = tk.Button(window, text="Kunden exportieren", command=lambda: export_customers_to_csv())
    export_button.pack()

    import_button = tk.Button(window, text="Kunden importieren", command=lambda: import_customers_from_csv())
    import_button.pack()

    notes_text = tk.Text(window, height=15)  
    notes_text.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    window.mainloop()


if __name__ == "__main__":
    main()
