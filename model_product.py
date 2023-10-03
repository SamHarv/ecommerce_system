

class Product:
    """Model class of product to create a Product object."""
    
    def __init__(self, pro_id="0000000", pro_model="SKUF00000", 
                 pro_category="default_category", 
                 pro_name="default_product_name",
                 pro_current_price="0.0", pro_raw_price="0.0", 
                 pro_discount="0", pro_likes_count="0"):
        """Constructor for Product class."""
        self.pro_id = pro_id
        self.pro_model = pro_model
        self.pro_category = pro_category
        self.pro_name = pro_name
        self.pro_current_price = pro_current_price
        self.pro_raw_price = pro_raw_price
        self.pro_discount = pro_discount
        self.pro_likes_count = pro_likes_count

    def __str__(self):
        """String representation of Product object."""
        return (f"{{'pro_id':'{self.pro_id}', 'pro_model':'{self.pro_model}', "
                f"'pro_category':'{self.pro_category}', "
                f"'pro_name':'{self.pro_name}', "
                f"'pro_current_price':'{self.pro_current_price}', "
                f"'pro_raw_price':'{self.pro_raw_price}', "
                f"'pro_discount':'{self.pro_discount}', "
                f"'pro_likes_count':'{self.pro_likes_count}'}}")
    
    def get_pro_id(self):
        return self.pro_id
    
    def get_pro_model(self):
        return self.pro_model
    
    def get_pro_category(self):
        return self.pro_category
    
    def get_pro_name(self):
        return self.pro_name
    
    def get_pro_current_price(self):
        return self.pro_current_price
    
    def get_pro_raw_price(self):
        return self.pro_raw_price
    
    def get_pro_discount(self):
        return self.pro_discount
    
    def get_pro_likes_count(self):
        return self.pro_likes_count
    
    def set_pro_id(self, pro_id):
        self.pro_id = pro_id

    def set_pro_model(self, pro_model):
        self.pro_model = pro_model

    def set_pro_category(self, pro_category):
        self.pro_category = pro_category

    def set_pro_name(self, pro_name):
        self.pro_name = pro_name

    def set_pro_current_price(self, pro_current_price):
        self.pro_current_price = pro_current_price

    def set_pro_raw_price(self, pro_raw_price):
        self.pro_raw_price = pro_raw_price

    def set_pro_discount(self, pro_discount):
        self.pro_discount = pro_discount

    def set_pro_likes_count(self, pro_likes_count):
        self.pro_likes_count = pro_likes_count