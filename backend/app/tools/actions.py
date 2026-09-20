from typing import Dict, Any, Optional

def calculate_delay_compensation(delay_hours: float) -> Dict[str, bool]:
    """
    Determines compensation based on delay hours.
    < 3 hours: meal voucher
    > 3 hours: meal voucher + lounge
    > 5 hours: meal voucher + lounge + hotel
    """
    compensation = {
        "meal_voucher": False,
        "lounge_access": False,
        "hotel_accommodation": False
    }
    
    if delay_hours > 5:
        compensation["hotel_accommodation"] = True
        compensation["lounge_access"] = True
        compensation["meal_voucher"] = True
    elif delay_hours > 3:
        compensation["lounge_access"] = True
        compensation["meal_voucher"] = True
    elif delay_hours > 0:
        compensation["meal_voucher"] = True
        
    return compensation

def validate_fare_difference(fare_difference: float) -> bool:
    """
    Returns True if fare difference is allowed without escalation.
    """
    return fare_difference <= 1500

def escalate_to_human(reason: str, booking_reference: str, **kwargs) -> Dict[str, Any]:
    """
    Escalate the case to a human supervisor.
    """
    escalation = {
        "status": "escalated",
        "reason": reason,
        "booking_reference": booking_reference,
    }
    escalation.update(kwargs)
    return escalation

def initiate_refund(booking_reference: str, is_airline_caused: bool) -> Dict[str, Any]:
    """
    Simulate processing a refund. Only allowed for airline-caused disruptions.
    """
    if not is_airline_caused:
        return escalate_to_human("Refund requested for non-airline-caused disruption", booking_reference)
        
    return {
        "status": "refund_initiated",
        "booking_reference": booking_reference,
        "refund_amount": "full",
        "payment_method": "original payment method",
        "processing_time": "7 business days"
    }

def rebook_customer(booking_reference: str, is_airline_caused: bool) -> Dict[str, Any]:
    """
    Simulate rebooking a customer. Only allowed for airline-caused cancellations at no charge.
    """
    if not is_airline_caused:
        return escalate_to_human("Free rebooking requested for non-airline-caused disruption", booking_reference)
        
    return {
        "status": "rebooking_confirmed",
        "booking_reference": booking_reference,
        "details": "Rebooked on the next available flight within 24 hours at no charge"
    }

def arrange_hotel(booking_reference: str, delay_hours: float) -> Dict[str, Any]:
    """
    Arrange hotel accommodation. Only valid if delay > 5 hours.
    """
    if delay_hours <= 5:
        return {
            "status": "denied",
            "reason": f"Hotel accommodation requires delay > 5 hours. Current delay is {delay_hours} hours."
        }
        
    return {
        "status": "hotel_arranged",
        "booking_reference": booking_reference,
        "coverage": "delayed hours only"
    }

def issue_meal_voucher(booking_reference: str) -> Dict[str, Any]:
    return {
        "status": "voucher_issued",
        "booking_reference": booking_reference,
        "type": "₹500 meal voucher"
    }

def grant_lounge_access(booking_reference: str) -> Dict[str, Any]:
    return {
        "status": "lounge_access_granted",
        "booking_reference": booking_reference
    }
