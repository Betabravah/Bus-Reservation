import os
import jwt
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from werkzeug.security import check_password_hash
from functools import wraps
from flask import request, jsonify, make_response


from model import db, User, Blacklist


class AuthenticationManager:
    """class used to manage authentication of a user"""

    def __init__(self, key: str, age: int = 259200) -> None:
        """
        Args:
            key (str): Encryption Key
            age (int): Age of a token before it expires
                        (Default value is 259200 seconds or 3 days)
        """
        self.age = age
        self.key = key


    def generate_jwt_token(self, data):
        """
        Generates signed authentication token for given payload data
        
        Args:
            data (Any): the data to be encoded using jwt
            
        Returns:
            str: a signed string that can later be loaded
        """
        data['exp'] = datetime.now() + timedelta(seconds=self.age)
        token =  jwt.encode(
            data,
            key=self.key,
            algorithm='HS256'
        )

        return token
    

    def verify_token(self, token: str):
        """
        Verifies and loads authentication token generated by jwt

        Args:
            token (str): authentication token to be verified

        Returns:
            Any: data from token if the token is valid, None otherwise
        """

        try:
            payload = jwt.decode(
                token,
                key = os.getenv('FLASK_SECRET_KEY'),
                algorithms='HS256'
            )
            return payload
        
        except ExpiredSignatureError:
            return None
        except InvalidSignatureError:
            return None
        
    def verify_credentials(self, email: str, password: str) -> bool:
        """
        Verifies the existence of given credentials in database

        Args:
            email (str): email of user
            password (str): password of user

        Returns:
            bool: True if email and password are valid, False otherwise
        """

        user = User.get_by_email(email)
        if not user:
            return False
        
        return check_password_hash(user.password, password)


    def load_user(token: str, secret_key=os.getenv('FLASK_SECRET_KEY')):
        """
        Validates user token and loads user from databse if user token is valid
        
        Args:
            token (str): user token generated by AuthenticationManager
            
        Returns:
            User: user object for which token belongs to, None otherwise"""
        
        auth_manager = AuthenticationManager(secret_key)
        user_id = auth_manager.verify_token(token)

        if user_id:
            user = User.get(user_id)
            if user.token == token:
                return user

auth_manager = AuthenticationManager(os.getenv('FLASK_SECRET_KEY'))

token = ""
current_user = ""

def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None

        if 'access-token' in request.headers:
            token = request.headers['access-token']

            if token:
                blacklist = Blacklist.get(token)
                if blacklist:
                    return make_response(
                        "Invalid Token",
                        401
                    )
            else:
                return make_response(
                    jsonify({'message': "A Valid Token is Missing!"}),
                    401
                )
            
        data = auth_manager.verify_token(token)
        if data:

            try:
                
                func.__globals__["current_user"] = User.get_by_id(data['id'])
                func.__globals__["token"] = token
                
                result =  func(*args, **kwargs)
                
                return result
            
            finally:
                func.__globals__.pop("current_user")
                func.__globals__.pop("token")
        
        else:
            return make_response(
                jsonify({'message': 'Invalid Token!'}),
                401
            )
        

    
    return decorator

