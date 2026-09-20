import pytest
from app.agent.graph import app_graph
from app.agent.state import AgentState
from app.tools.data_retrieval import get_customer_profile, get_booking_details

def test_priya_scenario():
    # Priya asks for refund and business class upgrade
    booking_ref = "SK4821X"
    customer = get_customer_profile(booking_ref)
    booking = get_booking_details(booking_ref)
    
    initial_state: AgentState = {
        "messages": [{"role": "user", "content": "I am furious! I want a full cash refund and a free business class upgrade on my return flight."}],
        "customer": customer,
        "booking": booking,
        "intent": None,
        "relevant_policy": None,
        "proposed_action": None,
        "policy_check": None,
        "tool_results": [],
        "escalation_required": False,
        "escalation_reason": None,
        "final_response": None
    }
    
    # In a full run, we'd mock the LLM if no API key is provided, 
    # but the test proves the logic flow works for cancellation refunds
    result = app_graph.invoke(initial_state)
    
    # Ensure it reaches the end
    assert result is not None
    # Action taken should be refund
    actions = [r.get("status") for r in result.get("tool_results", [])]
    assert "refund_initiated" in actions
