class Order:
    def __init__(self, order_id, stockname, trade_type, quantity):
        '''
        Initializes with the order information
        Arguments:
        - order_id: The transaction number of the order.
        - stockname: The name of the stock that was traded.
        - trade_type: The type of the trade.
        - quantity: The quantity that was traded.
        '''
        self.order_id = order_id # transaction number of the order
        self.stockname = stockname # name of the stock
        self.trade_type = trade_type # type of the trade
        self.quantity = quantity # qnatity traded
    
    def to_string(self):
        '''
        Function to convert the order object to string 
        :return order object attributes in a string form
        '''
        return f'{self.order_id},{self.stockname},{self.trade_type},{self.quantity}'

    def __str__(self):
        return self.to_string()

