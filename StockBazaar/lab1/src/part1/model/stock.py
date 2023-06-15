"""
Data model for storing Stock attributes
"""

class Stock:
    """
    Attributes:
    -----------
    name: name of the stock
    price: current stock price
    maxVolume : maximum allowed trading volume 
    volume : current volume of the stock in the market
    isTradable : the stock is tradable if the volume is below maximum allowed limit

    """
    def __init__(self, name, price):
        """
        Constructor 
        :param name: name of the stock
        :param price: stock price
        """
        self.name = name
        self.price = price
        self.maxVolume = 100
        self.volume = 0
        self.isTradable = True
