import pytest
import inventory_management as inv

d1 = inv.Inventory()

def test_add_stock():
    d1.add_stock("AAPL",10)
    assert d1.stock["AAPL"] == 10


# test add_stock function

def test_remove_stock():
    with pytest.raises(ValueError):
        d1.remove_stock("AAPL",12)

    d1.remove_stock("AAPL",8)
    assert d1.stock["AAPL"] == 2


# test remove stock function along with exception

def test_check_availability():
    assert d1.check_availability("AAPL",10) == False
    assert d1.check_availability("AAPL",2) == True


# test check_availability function

#def test_remove_stock_with_insufficient_inventory():


# rest exception situation in remove stock function

#def test_full_inventory_cycle():
# test entire cycle which is add_stock -> remove_stock -> check_availibility