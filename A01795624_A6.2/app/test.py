"""
Unit tests for the Hotel Reservation System.

This module contains tests for the Hotel, Customer, and Reservation.
"""

import unittest
import os
import json
from hotel import Hotel  # pylint: disable=import-error
from customer import Customer  # pylint: disable=import-error
from reservation import Reservation  # pylint: disable=import-error


class BaseTest(unittest.TestCase):
    """Base test class with shared setup and teardown logic."""

    def setUp(self):
        """Setup test files before each test."""
        self.hotel_data = []
        self.customer_data = []
        self.reservation_data = []
        self.create_test_files()

    def create_test_files(self):
        """Creates test JSON files with initial data."""
        with open(Hotel.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.hotel_data, f)
        with open(Customer.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.customer_data, f)
        with open(Reservation.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.reservation_data, f)

    def tearDown(self):
        """Removes test files after each test."""
        os.remove(Hotel.FILE_PATH)
        os.remove(Customer.FILE_PATH)
        os.remove(Reservation.FILE_PATH)


class TestCustomerSystem(BaseTest):
    """Unit tests for the Customer System."""

    def test_create_customer(self):
        """Test customer creation with valid email."""
        Customer.create_customer(1, "Victor Vazquez", "victorvazquez@tec.mx")
        customers = Customer.load_customers()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0]["email"], "victorvazquez@tec.mx")

    def test_create_customer_invalid_email(self):
        """Test customer creation with an invalid email."""
        with self.assertRaises(ValueError):
            Customer.create_customer(2, "Hugo Herrera", "invalid-email")

    def test_create_duplicate_customer(self):
        """Test that duplicate customer IDs are not allowed."""
        Customer.create_customer(1, "Victor", "victorvazquez@tec.mx")
        with self.assertRaises(ValueError):
            Customer.create_customer(1, "Victor", "victorvazquez@tec.mx")

    def test_delete_non_existent_customer(self):
        """Test deleting a non-existent customer should not crash."""
        initial_count = len(Customer.load_customers())
        Customer.delete_customer(99)
        self.assertEqual(len(Customer.load_customers()), initial_count)

    def test_modify_non_existent_customer(self):
        """Test modifying a non-existent customer should not crash."""
        Customer.modify_customer(99, "Updated Name", "updated@example.com")
        customers = Customer.load_customers()
        self.assertFalse(any(c["customer_id"] == 99 for c in customers))


class TestHotelSystem(BaseTest):
    """Unit tests for the Hotel System."""

    def test_create_hotel_invalid_rooms(self):
        """Test hotel creation with negative room numbers."""
        with self.assertRaises(ValueError):
            Hotel.create_hotel(2, "Invalid Hotel", "Test City", -5)

    def test_create_duplicate_hotel(self):
        """Test that duplicate hotel IDs are not allowed."""
        Hotel.create_hotel(1, "Test Hotel", "Test City", 10)
        with self.assertRaises(ValueError):
            Hotel.create_hotel(1, "Duplicate Hotel", "Another City", 15)

    def test_delete_non_existent_hotel(self):
        """Test deleting a non-existent hotel should not crash."""
        initial_count = len(Hotel.load_hotels())
        Hotel.delete_hotel(99)
        self.assertEqual(len(Hotel.load_hotels()), initial_count)

    def test_modify_non_existent_hotel(self):
        """Test modifying a non-existent hotel should not crash."""
        Hotel.modify_hotel(99, "Updated Name", "Updated Location", 20)
        hotels = Hotel.load_hotels()
        self.assertFalse(any(h["hotel_id"] == 99 for h in hotels))

    def test_reserve_room_no_availability(self):
        """Test that reserving a room in a full hotel fails gracefully."""
        Hotel.create_hotel(3, "Small Hotel", "Test City", 1)
        Hotel.reserve_room(3)  # First room reservation
        with self.assertRaises(ValueError) as context:
            Hotel.reserve_room(3)  # Second reservation should fail
        self.assertEqual(str(context.exception), "No available rooms.")


class TestReservationSystem(BaseTest):
    """Unit tests for the Reservation System."""

    def test_create_customer(self):
        """Test customer creation with valid email."""
        Customer.create_customer(1, "Victor Vazquez", "victorvazquez@tec.mx")
        customers = Customer.load_customers()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0]["email"], "victorvazquez@tec.mx")

    def test_create_hotel(self):
        """Test hotel creation."""
        Hotel.create_hotel(1, "Test Hotel", "Test Location", 10)
        hotels = Hotel.load_hotels()
        self.assertEqual(len(hotels), 1)
        self.assertEqual(hotels[0]["name"], "Test Hotel")

    def test_create_reservation(self):
        """Test reservation creation when customer and hotel exist."""
        Hotel.create_hotel(1, "Test Hotel", "Test Location", 10)
        Customer.create_customer(1, "Victor Vazquez", "victorvazquez@tec.mx")
        Reservation.create_reservation(1, 1, 1)
        reservations = Reservation.load_reservations()
        self.assertEqual(len(reservations), 1)
        self.assertEqual(reservations[0]["customer_id"], 1)

    def test_create_reservation_invalid_customer(self):
        """Test reservation creation failure when customer ID doesn't exist."""
        Hotel.create_hotel(1, "Test Hotel", "Test Location", 10)
        with self.assertRaises(ValueError):
            Reservation.create_reservation(1, 99, 1)

    def test_create_reservation_invalid_hotel(self):
        """Test reservation creation failure when hotel ID does not exist."""
        Customer.create_customer(1, "John Doe", "john@example.com")
        with self.assertRaises(ValueError):
            Reservation.create_reservation(1, 1, 99)

    def test_cancel_reservation(self):
        """Test canceling a reservation."""
        Hotel.create_hotel(1, "Test Hotel", "Test Location", 10)
        Customer.create_customer(1, "Victor Vazquez", "victorvazquez@tec.mx")
        Reservation.create_reservation(1, 1, 1)
        Reservation.cancel_reservation(1)
        reservations = Reservation.load_reservations()
        self.assertEqual(len(reservations), 0)


if __name__ == "__main__":
    unittest.main()
