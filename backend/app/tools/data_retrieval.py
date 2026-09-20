import json
import os
from typing import Dict, Any, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

def get_customer_profile(booking_reference: str) -> Optional[Dict[str, Any]]:
    """
    Returns the customer associated with the booking reference.
    """
    try:
        with open(os.path.join(DATA_DIR, "customers.json"), "r", encoding="utf-8") as f:
            customers = json.load(f)
            for customer in customers:
                if customer.get("booking_reference") == booking_reference:
                    return customer
    except FileNotFoundError:
        pass
    return None

def get_booking_details(booking_reference: str) -> Optional[Dict[str, Any]]:
    """
    Returns booking details including customer, flight, route, date, departure time, and status.
    """
    try:
        with open(os.path.join(DATA_DIR, "bookings.json"), "r", encoding="utf-8") as f:
            bookings = json.load(f)
            for booking in bookings:
                if booking.get("booking_reference") == booking_reference:
                    return booking
    except FileNotFoundError:
        pass
    return None
