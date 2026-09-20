import pytest
from app.agent.graph import app_graph
from app.tools.actions import calculate_delay_compensation, validate_fare_difference, initiate_refund, rebook_customer
from app.tools.data_retrieval import get_customer_profile, get_booking_details


def test_priya_cancellation_scenario():
    booking_ref = "SK4821X"
    customer = get_customer_profile(booking_ref)
    booking = get_booking_details(booking_ref)
    result = app_graph.invoke({
        "messages": [{"role": "user", "content": "I am furious! I want a full cash refund and a free business class upgrade on my return flight for the trouble."}],
        "customer": customer,
        "booking": booking,
        "intent": None,
        "relevant_policy": None,
        "proposed_action": None,
        "policy_check": None,
        "tool_results": [],
        "escalation_required": False,
        "escalation_reason": None,
        "final_response": None,
    })
    response = (result.get("final_response") or "").lower()
    assert "refund" in response
    assert "business" in response or "upgrade" in response


def test_arvind_delay_scenario():
    booking_ref = "TR1190B"
    customer = get_customer_profile(booking_ref)
    booking = get_booking_details(booking_ref)
    result = app_graph.invoke({
        "messages": [{"role": "user", "content": "I am frustrated and need hotel accommodation since it has been such a long delay."}],
        "customer": customer,
        "booking": booking,
        "intent": None,
        "relevant_policy": None,
        "proposed_action": None,
        "policy_check": None,
        "tool_results": [],
        "escalation_required": False,
        "escalation_reason": None,
        "final_response": None,
    })
    response = (result.get("final_response") or "").lower()
    assert "meal" in response or "lounge" in response
    assert "hotel" in response


def test_meher_fare_difference_and_hotel_request():
    booking_ref = "WL7742"
    customer = get_customer_profile(booking_ref)
    booking = get_booking_details(booking_ref)
    result = app_graph.invoke({
        "messages": [{"role": "user", "content": "I want a full night's hotel stay and a different higher-fare flight. The fare difference is ₹2,000."}],
        "customer": customer,
        "booking": booking,
        "intent": None,
        "relevant_policy": None,
        "proposed_action": None,
        "policy_check": None,
        "tool_results": [],
        "escalation_required": False,
        "escalation_reason": None,
        "final_response": None,
    })
    response = (result.get("final_response") or "").lower()
    assert "supervisor" in response or "escalat" in response
    assert "₹2,000" in response or "2000" in response or "fare difference" in response


def test_delay_compensation():
    # 2 hours: meal
    comp_2h = calculate_delay_compensation(2)
    assert comp_2h["meal_voucher"] is True
    assert comp_2h["lounge_access"] is False
    assert comp_2h["hotel_accommodation"] is False

    # 4 hours: meal + lounge
    comp_4h = calculate_delay_compensation(4)
    assert comp_4h["meal_voucher"] is True
    assert comp_4h["lounge_access"] is True
    assert comp_4h["hotel_accommodation"] is False

    # 6 hours: meal + lounge + hotel
    comp_6h = calculate_delay_compensation(6)
    assert comp_6h["meal_voucher"] is True
    assert comp_6h["lounge_access"] is True
    assert comp_6h["hotel_accommodation"] is True

def test_fare_difference():
    assert validate_fare_difference(1000) is True
    assert validate_fare_difference(1500) is True
    assert validate_fare_difference(2000) is False

def test_cancellation_actions():
    # Airline caused
    refund = initiate_refund("TEST", True)
    assert refund["status"] == "refund_initiated"
    
    # Not airline caused
    refund_bad = initiate_refund("TEST", False)
    assert refund_bad["status"] == "escalated"
