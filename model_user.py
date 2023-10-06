

class User:
    """User class is the base for Customer and Admin classes."""

    def __init__(self, user_id="u_0000000000", user_name="default_user",
                 user_password="a0000",
                 user_register_time="00-00-0000_00:00:00",
                 user_role="customer"):
        """Constructor for User class."""
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = user_password
        self.user_register_time = user_register_time
        self.user_role = user_role

    def __str__(self):
        """String representation of User object."""
        return (f"{{'user_id':'{self.user_id}', "
                f"'user_name':'{self.user_name}', "
                f"'user_password':'{self.user_password}', "
                f"'user_register_time':'{self.user_register_time}', "
                f"'user_role':'{self.user_role}'}}")
