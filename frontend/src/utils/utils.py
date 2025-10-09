class Utils:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        import re

        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email) is not None

    @staticmethod
    def hash_password(password: str) -> str:
        import hashlib

        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def format_date(date_obj, format_str="%Y-%m-%d") -> str:
        return date_obj.strftime(format_str)

    @staticmethod
    def parse_date(date_str: str, format_str="%Y-%m-%d"):
        from datetime import datetime

        return datetime.strptime(date_str, format_str)

    @staticmethod
    def generate_random_string(length: int = 12) -> str:
        import random
        import string

        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    @staticmethod
    def capitalize_words(text: str) -> str:
        return " ".join(word.capitalize() for word in text.split())
