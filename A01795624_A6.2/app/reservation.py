"""
Reservation Management Module

This module provides functions to manage hotel reservations, including
creating and canceling reservations. It validates customer and hotel existence
before processing reservations.
"""

import json
import os
from typing import Dict, List
from hotel import Hotel  # pylint: disable=import-error
from customer import Customer  # pylint: disable=import-error


class Reservation:
    """Reservation Management Class for managing hotel reservations."""

    FILE_PATH = "data/reservations.json"

    def __init__(self, reservation_id: int, customer_id: int, hotel_id: int):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self) -> Dict:
        """Converts Reservation object to dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id
        }

    @staticmethod
    def load_reservations() -> List[Dict]:
        """Loads reservation data from file."""
        if os.path.exists(Reservation.FILE_PATH):
            with open(Reservation.FILE_PATH, "r", encoding="UTF-8") as file:
                return json.load(file)
        return []

    @staticmethod
    def save_reservations(reservations: List[Dict]) -> None:
        """Saves reservation data to file."""
        with open(Reservation.FILE_PATH, "w", encoding="UTF-8") as file:
            json.dump(reservations, file, indent=4)

    @staticmethod
    def customer_exists(customer_id: int) -> bool:
        """Checks if a customer exists in customers.json."""
        customers = Customer.load_customers()
        return any(
            customer["customer_id"] == customer_id for customer in customers
        )

    @staticmethod
    def hotel_exists(hotel_id: int) -> bool:
        """Checks if a hotel exists in hotels.json."""
        hotels = Hotel.load_hotels()
        return any(
            hotel["hotel_id"] == hotel_id for hotel in hotels
        )

    @classmethod
    def create_reservation(cls, reservation_id: int,
                           customer_id: int, hotel_id: int):
        """Creates a new reservation."""
        if not cls.customer_exists(customer_id):
            raise ValueError(f"Error: CustomerID {customer_id} doesn't exist.")

        if not cls.hotel_exists(hotel_id):
            raise ValueError(f"Error: Hotel ID {hotel_id} does not exist.")

        reservations = cls.load_reservations()
        if any(r["reservation_id"] == reservation_id for r in reservations):
            raise ValueError(f"Error: Reservation ID {reservation_id} "
                             f"already exists.")

        new_reservation = cls(reservation_id, customer_id, hotel_id)
        reservations.append(new_reservation.to_dict())

        customers = Customer.load_customers()
        for customer in customers:
            if customer["customer_id"] == customer_id:
                customer["reservation_id"] = reservation_id
                customer["has_reservation"] = True
                break
        Customer.save_customers(customers)

        cls.save_reservations(reservations)
        print("Reservation created successfully.")

    @classmethod
    def cancel_reservation(cls, reservation_id: int):
        """Cancels a reservation and updates the
        customer's reservation status."""
        reservations = [
            r for r in cls.load_reservations()
            if r["reservation_id"] != reservation_id
        ]

        customers = Customer.load_customers()
        for customer in customers:
            if customer.get("reservation_id") == reservation_id:
                customer["reservation_id"] = None
                customer["has_reservation"] = False
                break
        Customer.save_customers(customers)

        cls.save_reservations(reservations)
        print("Reservation canceled successfully.")
