"""
Customer Management Module

This module provides functions to manage customer data, including
creating, modifying, deleting, and displaying customer information.
"""

import json
import os
from typing import Dict, List


class Customer:
    """Customer Management Class for managing customer data."""

    FILE_PATH = "data/customers.json"

    def __init__(self, customer_id: int, name: str, email: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self) -> Dict:
        """Converts Customer instance to a dictionary."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email
        }

    @staticmethod
    def load_customers() -> List[Dict]:
        """Loads customer data from file."""
        if os.path.exists(Customer.FILE_PATH):
            with open(Customer.FILE_PATH, "r", encoding="UTF-8") as file:
                return json.load(file)
        return []

    @staticmethod
    def save_customers(customers: List[Dict]) -> None:
        """Saves customer data to file."""
        with open(Customer.FILE_PATH, "w", encoding="UTF-8") as file:
            json.dump(customers, file, indent=4)

    @classmethod
    def create_customer(cls, customer_id: int, name: str, email: str):
        """Creates a new customer and saves to file."""
        if "@" not in email or "." not in email:
            raise ValueError(f"Invalid email: {email}")
        customers = cls.load_customers()
        if any(c["customer_id"] == customer_id for c in customers):
            raise ValueError(f"Customer ID {customer_id} already exists.")
        customers.append(cls(customer_id, name, email).to_dict())
        cls.save_customers(customers)

    @classmethod
    def delete_customer(cls, customer_id: int):
        """Deletes a customer from file."""
        customers = cls.load_customers()
        customers = [c for c in customers if c["customer_id"] != customer_id]
        cls.save_customers(customers)

    @classmethod
    def display_customers(cls):
        """Displays all customers."""
        customers = cls.load_customers()
        for customer in customers:
            print(customer)

    @classmethod
    def modify_customer(
            cls, customer_id: int, name: str, email: str,
            reservation_id: int = None
    ):
        """Modifies an existing customer's information."""
        customers = cls.load_customers()
        for customer in customers:
            if customer["customer_id"] == customer_id:
                customer["name"] = name
                customer["email"] = email
                customer["reservation_id"] = reservation_id
                customer["has_reservation"] = reservation_id is not None
                break
        cls.save_customers(customers)
