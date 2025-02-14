"""
Hotel Management Module

This module provides functions to manage hotel data, including
creating, modifying, deleting, and displaying hotel information.
It also supports room reservations and cancellations.
"""

import json
import os
from typing import Dict, List


class Hotel:
    """Hotel Management Class for managing hotel data."""

    FILE_PATH = "data/hotels.json"

    def __init__(self, hotel_id: int, name: str, location: str, rooms: int):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = rooms
        self.available_rooms = rooms

    def to_dict(self) -> Dict:
        """Converts Hotel object to dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "rooms": self.rooms,
            "available_rooms": self.available_rooms
        }

    @staticmethod
    def load_hotels() -> List[Dict]:
        """Loads hotel data from the file."""
        if os.path.exists(Hotel.FILE_PATH):
            with open(Hotel.FILE_PATH, "r", encoding="UTF-8") as file:
                return json.load(file)
        return []

    @staticmethod
    def save_hotels(hotels: List[Dict]) -> None:
        """Saves hotel data to the file."""
        with open(Hotel.FILE_PATH, "w", encoding="UTF-8") as file:
            json.dump(hotels, file, indent=4)

    @classmethod
    def create_hotel(cls, hotel_id: int, name: str, location: str, rooms: int):
        """Creates a new hotel and saves it to file."""
        if rooms < 0:
            raise ValueError("Number of rooms cannot be negative.")

        hotels = cls.load_hotels()
        if any(h["hotel_id"] == hotel_id for h in hotels):
            raise ValueError(f"Hotel ID {hotel_id} already exists.")

        hotels.append(cls(hotel_id, name, location, rooms).to_dict())
        cls.save_hotels(hotels)

    @classmethod
    def delete_hotel(cls, hotel_id: int):
        """Deletes a hotel from the file."""
        hotels = cls.load_hotels()
        hotels = [h for h in hotels if h["hotel_id"] != hotel_id]
        cls.save_hotels(hotels)

    @classmethod
    def display_hotels(cls):
        """Displays all hotels."""
        hotels = cls.load_hotels()
        for hotel in hotels:
            print(hotel)

    @classmethod
    def modify_hotel(cls, hotel_id: int, name: str, location: str, rooms: int):
        """Modifies an existing hotel's information."""
        hotels = cls.load_hotels()
        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                hotel["name"] = name
                hotel["location"] = location
                hotel["rooms"] = rooms
                hotel["available_rooms"] = rooms
                break
        cls.save_hotels(hotels)

    @classmethod
    def reserve_room(cls, hotel_id: int):
        """Reserves a room in a hotel if available."""
        hotels = cls.load_hotels()
        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                if hotel["available_rooms"] > 0:
                    hotel["available_rooms"] -= 1
                    cls.save_hotels(hotels)
                    return
                raise ValueError("No available rooms.")
        raise ValueError("Hotel not found.")

    @classmethod
    def cancel_reservation(cls, hotel_id: int):
        """Cancels a room reservation, increasing available rooms."""
        hotels = cls.load_hotels()
        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                if hotel["available_rooms"] < hotel["rooms"]:
                    hotel["available_rooms"] += 1
                    cls.save_hotels(hotels)
                    print(f"Reservation canceled at {hotel['name']}.")
                else:
                    print("No reservations to cancel.")
                return
        print("Hotel not found.")
