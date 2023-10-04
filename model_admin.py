from model_user import User


class Admin(User):
    """Admin class inherits from User class to create an Admin object."""
    
    def __init__(self, user_id="u_0000000000", user_name="default_user", 
                 user_password="a0000", 
                 user_register_time="00-00-0000_00:00:00", 
                 user_role="admin"):
        """Constructor for Admin class."""
        super().__init__(user_id, user_name, user_password, user_register_time, 
                         user_role)
    
    def __str__(self):
        """String representation of Admin object."""
        return (f"{{'user_id':'{self.user_id}', "
                f"'user_name':'{self.user_name}', " 
                f"'user_password':'{self.user_password}', " 
                f"'user_register_time':'{self.user_register_time}', " 
                f"'user_role':'{self.user_role}'}}")