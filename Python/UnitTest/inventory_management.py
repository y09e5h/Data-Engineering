#%%
class Inventory:
    def __init__(self):
        self.stock = {}

    def add_stock(self, item, quantity):
        if item in self.stock:
            self.stock[item] += quantity
        else:
            self.stock[item] = quantity

    def remove_stock(self, item, quantity):
        if item not in self.stock or self.stock[item] < quantity:
            raise ValueError("Insufficient stock")
        self.stock[item] -= quantity

    def check_availability(self, item, quantity):
        return self.stock.get(item, 0) >= quantity