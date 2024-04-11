class Order:
    def __init__(self,order_id='o_00000',user_id='u_0000000000',product_id='',order_time='00-00-0000_00:00:00',order_price=0.0):
        self.order_id = order_id
        self.user_id = user_id
        self.product_id = product_id
        self.order_time =order_time
        self.order_price =order_price
    def __str__(self):
        return f"{{'order_id':'{self.order_id}','user_id':'{self.user_id}','product_id':'{self.product_id}','order_time':'{self.order_time}','order_price':{self.order_price}}}"
