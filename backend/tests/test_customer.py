import pytest
from app.tools.data_retrieval import get_customer_profile

def test_get_customer_profile():
    # Test Priya
    priya = get_customer_profile("SK4821X")
    assert priya is not None
    assert priya["name"] == "Priya Nair"
    
    # Test Arvind
    arvind = get_customer_profile("TR1190B")
    assert arvind is not None
    assert arvind["name"] == "Arvind Kulkarni"
    
    # Test Meher
    meher = get_customer_profile("WL7742")
    assert meher is not None
    assert meher["name"] == "Meher Kaur"
    
    # Test invalid
    invalid = get_customer_profile("INVALID")
    assert invalid is None
