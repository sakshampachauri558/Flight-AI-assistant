import pytest
from app.tools.data_retrieval import get_booking_details

def test_get_booking_details():
    priya_booking = get_booking_details("SK4821X")
    assert priya_booking is not None
    assert priya_booking["flight"] == "SK-204"
    assert priya_booking["status"] == "Cancelled"
    
    arvind_booking = get_booking_details("TR1190B")
    assert arvind_booking is not None
    assert arvind_booking["status"] == "Delayed 4 hours"
