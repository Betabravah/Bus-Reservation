from model import User


class Authenication:
    """class used to manage authentication of a user"""

    def __init__(self, key: str, age: int = 604800) -> None:
        """
        Args:
            key (str): Encryption Key
            age (int): Age of a token before it expires
                        (Default value is 604800 seconds or 7 days)
        """

        
