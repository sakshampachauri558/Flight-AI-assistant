from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    customer: Optional[Dict[str, Any]]
    booking: Optional[Dict[str, Any]]
    intent: Optional[str]
    relevant_policy: Optional[str]
    proposed_action: Optional[str]
    policy_check: Optional[bool]
    tool_results: List[Dict[str, Any]]
    escalation_required: bool
    escalation_reason: Optional[str]
    final_response: Optional[str]
