"""
Hotel Reservation System

This script provides an interactive console-based system for
hotels, customers, and reservations.
"""

from hotel import Hotel  # pylint: disable=import-error
from customer import Customer  # pylint: disable=import-error
from reservation import Reservation  # pylint: disable=import-error


def hotel_menu():
    """Menu for managing hotels."""
    while True:
        print("\nHotel Menu:")
        print("1. Create Hotel")
        print("2. Delete Hotel")
        print("3. Display Hotels")
        print("4. Modify Hotel Information")
        print("5. Reserve a Room")
        print("6. Cancel a Reservation")
        print("7. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            hotel_id = int(input("Enter Hotel ID: "))
            hotels = Hotel.load_hotels()
            if any(h["hotel_id"] == hotel_id for h in hotels):
                print("Error: Hotel ID already exists.")
                continue
            name = input("Enter Hotel Name: ")
            location = input("Enter Location: ")
            rooms = int(input("Enter Number of Rooms: "))
            Hotel.create_hotel(hotel_id, name, location, rooms)
        elif choice == "2":
            hotel_id = int(input("Enter Hotel ID to delete: "))
            Hotel.delete_hotel(hotel_id)
        elif choice == "3":
            Hotel.display_hotels()
        elif choice == "4":
            hotel_id = int(input("Enter Hotel ID to modify: "))
            name = input("Enter new Hotel Name: ")
            location = input("Enter new Location: ")
            rooms = int(input("Enter new Number of Rooms: "))
            Hotel.modify_hotel(hotel_id, name, location, rooms)
        elif choice == "5":
            hotel_id = int(input("Enter Hotel ID to reserve a room: "))
            Hotel.reserve_room(hotel_id)
        elif choice == "6":
            hotel_id = int(input("Enter Hotel ID to cancel a reservation: "))
            Hotel.cancel_reservation(hotel_id)
        elif choice == "7":
            break
        else:
            print("Invalid option, please try again.")


def customer_menu():
    """Menu for managing customers."""
    while True:
        print("\nCustomer Menu:")
        print("1. Create Customer")
        print("2. Delete Customer")
        print("3. Display Customers")
        print("4. Modify Customer Information")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            customer_id = int(input("Enter Customer ID: "))
            customers = Customer.load_customers()
            if any(c["customer_id"] == customer_id for c in customers):
                print("Error: Customer ID already exists.")
                continue
            name = input("Enter Customer Name: ")
            while True:
                email = input("Enter Email: ")
                if "@" in email and "." in email:
                    break
                print("Error: Invalid email format. Please enter a valid one.")
            Customer.create_customer(customer_id, name, email)
        elif choice == "2":
            customer_id = int(input("Enter Customer ID to delete: "))
            Customer.delete_customer(customer_id)
        elif choice == "3":
            Customer.display_customers()
        elif choice == "4":
            customer_id = int(input("Enter Customer ID to modify: "))
            name = input("Enter new Customer Name: ")
            email = input("Enter new Email: ")
            Customer.modify_customer(customer_id, name, email)
        elif choice == "5":
            break
        else:
            print("Invalid option, please try again.")


def reservation_menu():
    """Menu for managing reservations."""
    while True:
        print("\nReservation Menu:")
        print("1. Create Reservation")
        print("2. Cancel Reservation")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            res_id = int(input("Enter Reservation ID: "))
            reservations = Reservation.load_reservations()
            if any(r["res_id"] == res_id for r in reservations):
                print("Error: Reservation ID already exists.")
                continue
            customer_id = int(input("Enter Customer ID: "))
            hotel_id = int(input("Enter Hotel ID: "))
            Reservation.create_reservation(res_id, customer_id, hotel_id)
        elif choice == "2":
            res_id = int(input("Enter Reservation ID to cancel: "))
            Reservation.cancel_reservation(res_id)
        elif choice == "3":
            break
        else:
            print("Invalid option, please try again.")


def main():
    """Main function to interact with the reservation system."""
    print("Welcome to the Hotel Reservation System")
    while True:
        print("\nSelect an entity:")
        print("1. Hotel")
        print("2. Customer")
        print("3. Reservation")
        print("4. Exit")

        entity_choice = input("Enter your choice: ")

        if entity_choice == "1":
            hotel_menu()
        elif entity_choice == "2":
            customer_menu()
        elif entity_choice == "3":
            reservation_menu()
        elif entity_choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
