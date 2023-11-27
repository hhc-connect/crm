from database import add_customer, list_customers, search_customers, delete_customer, update_customer_statuses

def show_menu():
    print("\nCRM-System - Hauptmenü")
    print("1. Neuen Kunden anlegen")
    print("2. Kunden suchen")
    print("3. Alle Kunden anzeigen")
    print("4. Kundenstatus aktualisieren")
    print("5. Kunden löschen")
    print("6. Beenden")
    return input("Wählen Sie eine Option: ")

def interact_add_customer():
    print("Neuen Kunden anlegen:")
    name = input("Name: ")
    email = input("E-Mail: ")
    phone = input("Telefon: ")
    address = input("Adresse: ")
    note = input("Notiz: ")
    add_customer(name, email, phone, address, note)
    print("Kunde hinzugefügt.")

def interact_search_customers():
    print("Kunden suchen:")
    name = input("Name (optional): ")
    email = input("E-Mail (optional): ")
    phone = input("Telefon (optional): ")
    address = input("Adresse (optional): ")
    results = search_customers(name, email, phone, address)
    if results:
        for customer in results:
            print(f"ID: {customer['id']}, Name: {customer['name']}, E-Mail: {customer['email']}, Telefon: {customer['phone']}, Adresse: {customer['address']}, Notiz: {customer['note']}")
    else:
        print("Keine Kunden gefunden, die den Kriterien entsprechen.")

def interact_list_all_customers():
    print("Alle Kunden anzeigen:")
    customers = list_customers()
    for customer in customers:
        print(f"ID: {customer['id']}, Name: {customer['name']}, E-Mail: {customer['email']}, Telefon: {customer['phone']}, Adresse: {customer['address']}, Notiz: {customer['note']}")

def interact_update_customer_statuses():
    print("Kundenstatus aktualisieren:")
    update_customer_statuses()
    print("Kundenstatus aktualisiert.")

def interact_delete_customer():
    customer_id = input("Geben Sie die Kunden-ID ein, die Sie löschen möchten: ")
    delete_customer(customer_id)
    print(f"Kunde mit ID {customer_id} wurde gelöscht.")

def main():
    while True:
        choice = show_menu()
        if choice == "1":
            interact_add_customer()
        elif choice == "2":
            interact_search_customers()
        elif choice == "3":
            interact_list_all_customers()
        elif choice == "4":
            interact_update_customer_statuses()
        elif choice == "5":
            interact_delete_customer()
        elif choice == "6":
            print("Programm beendet.")
            break

if __name__ == "__main__":
    main()
