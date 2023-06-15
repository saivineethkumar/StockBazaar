import decimal


class Stock:
    def __init__(self, name, price, vol):
        ''' Constructor
        :param name: name of the stock
        :param price: price of the stock
        :param vol: current volume of the stock in the market
        '''
        self.name = name
        # define price as a decimal with precision of 2 decimal places
        self.price = decimal.Decimal(str(price)).quantize(
            decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)
        self.volume = vol

    def getPrice(self):
        '''
        Function to return the price of the stock object
        :return price of the stock as float
        '''
        return float(self.price)


    def trade(self, quantity, trade_type):
        '''
        Function to perform trading on the stock.
        :param quantity: quantity of the stock being traded
        :param trade_type:  type of the trade. Either BUY or SELL
        :return 1 if trade is success, 0 if trade cannot be processes due to insufficient quantity and -1 in case of any error/exceptions or quantity negative
        '''
        try:
            quantity = int(quantity)
            # trade_type = 0 for BUY and 1 for SELL
            # trade type BUY and quantity is sufficient to perform trade
            if(trade_type == 0 and quantity>=0 and self.volume >= quantity):
                self.volume -= quantity
                return 1
            # trade type BUY and quantity is insufficient to perform trade
            elif(trade_type == 0 and quantity>=0 and self.volume < quantity):
                return 0
            # trade tyoe SELL and quantity is > 0
            elif ( trade_type == 1 and quantity >= 0):
                self.volume += quantity
                return 1
        except Exception as e:
            print(f'Failed to initiate trade for stock: {self.name} with exception : {e}')
        return -1

    def to_string(self):
        '''
        Function to convert the stock object to string 
        :return stock object attributes in a string form
        '''
        return f'{self.name},{self.getPrice()},{self.volume}'

    def __str__(self):
        return self.to_string()
