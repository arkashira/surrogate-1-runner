class Component:
    def __init__(self, name, model, price, link):
        self.name = name
        self.model = model
        self.price = price
        self.link = link

class CPU(Component):
    def __init__(self, name, model, price, link, socket):
        super().__init__(name, model, price, link)
        self.socket = socket

class Motherboard(Component):
    def __init__(self, name, model, price, link, socket, form_factor):
        super().__init__(name, model, price, link)
        self.socket = socket
        self.form_factor = form_factor

class GPU(Component):
    def __init__(self, name, model, price, link, wattage):
        super().__init__(name, model, price, link)
        self.wattage = wattage

class PSU(Component):
    def __init__(self, name, model, price, link, wattage):
        super().__init__(name, model, price, link)
        self.wattage = wattage

class Case(Component):
    def __init__(self, name, model, price, link, form_factor):
        super().__init__(name, model, price, link)
        self.form_factor = form_factor