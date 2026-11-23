from services.reorder import calculate_reorder

def test_reorder_quantity():
    assert calculate_reorder(5, 12, 3) == 10
    assert calculate_reorder(20, 12, 3) == 0
