import decimal


class Stock:
    def __init__(self, name, price):
        ''' Constructor
        :param name: name of the stock
        :param price: price of the stock
        '''
        self.name = name
        # define price as a decimal with precision of 2 decimal places
        self.price = decimal.Decimal(str(price)).quantize(
            decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)
        self.maxVolume = 100
        self.volume = 0
        self.isTradable = True  # a flag indicating if the stock is currently tradable

    def getPrice(self):
        '''
        Function to return the price of the stock object
        :return price of the stock as float
        '''
        return float(self.price)

    def updatePrice(self, price):
        '''
        Function to update the price of the stock
        :param price: new price of the stock
        :return True if update is successfull, False otherwise
        '''
        try:
            if (isinstance(price, float) and price >= 0):
                # storing price as a decimal with precision of 2 decimal places
                price = decimal.Decimal(str(price)).quantize(
                    decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)
                self.price = price
                return True
        except Exception as e:
            print(
                f'Failed to parse and update price for stock : {self.name} with exception: {e}')
        return False

    def trade(self, quantity, type):
        '''
        Function to perform trading on the stock. Updates the isTradable flag to False if the maxVolume is reached
        :param quantity: quantity of the stock being traded
        :param type:  type of the trade. Either BUY or SELL
        :return True if the trade is successfull, False otherwise
        '''
        try:
            quantity = int(quantity)
            if (quantity >= 0 and self.volume + quantity <= self.maxVolume):
                self.volume += quantity
                return True
            self.isTradable = False
        except Exception as e:
            print(
                f'Failed to initiate trade for stock: {self.name} with exception : {e}')
        return False
