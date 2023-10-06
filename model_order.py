

class Order:
    """Model class for creation of Order object."""
    
    def __init__(self, order_id="o_00000", user_id="u_0000000000", 
                 pro_id="0000000", order_time="00-00-0000_00:00:00"):
        """Constructor for Order class."""
        self.order_id = order_id
        self.user_id = user_id
        self.pro_id = pro_id
        self.order_time = order_time

    def __str__(self):
        """String representation of Order object."""
        return (f"{{'order_id':'{self.order_id}', 'user_id':'{self.user_id}', "
                f"'pro_id':'{self.pro_id}', "
                f"'order_time':'{self.order_time}'}}")