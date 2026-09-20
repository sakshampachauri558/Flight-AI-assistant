from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import ChatRequest, ChatResponse
from app.tools.data_retrieval import get_customer_profile, get_booking_details
from app.agent.graph import app_graph
from app.agent.state import AgentState

app = FastAPI(title="Airline Resolution Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/customer/{booking_reference}")
def get_customer(booking_reference: str):
    customer = get_customer_profile(booking_reference)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/api/booking/{booking_reference}")
def get_booking(booking_reference: str):
    booking = get_booking_details(booking_reference)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    customer = get_customer_profile(request.booking_reference)
    booking = get_booking_details(request.booking_reference)
    
    if not customer or not booking:
        raise HTTPException(status_code=404, detail="Invalid booking reference")
        
    initial_state: AgentState = {
        "messages": [{"role": "user", "content": request.message}],
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
    
    result = app_graph.invoke(initial_state)
    
    actions = [res.get("status") for res in result.get("tool_results", []) if res.get("status")]
    
    return ChatResponse(
        response=result.get("final_response", "Sorry, I couldn't process that."),
        escalated=result.get("escalation_required", False),
        actions_taken=actions,
        policies_applied=["Cancellation Rule" if "Cancelled" in booking.get("status", "") else "Delay Compensation"]
    )
