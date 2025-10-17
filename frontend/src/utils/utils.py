from datetime import datetime


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
    def format_date(date_str: str) -> str:
        """Format date string to DD/MM/YYYY"""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%d/%m/%Y")
        except:
            return date_str

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

    @staticmethod
    def trunc_text(text: str, length: int = 7) -> str:
        return text[:length] + "..." if len(text) > length else text

    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for search (remove accents, etc.)"""
        replacements = {
            "à": "a",
            "á": "a",
            "â": "a",
            "ã": "a",
            "ä": "a",
            "å": "a",
            "è": "e",
            "é": "e",
            "ê": "e",
            "ë": "e",
            "ì": "i",
            "í": "i",
            "î": "i",
            "ï": "i",
            "ò": "o",
            "ó": "o",
            "ô": "o",
            "õ": "o",
            "ö": "o",
            "ù": "u",
            "ú": "u",
            "û": "u",
            "ü": "u",
            "ç": "c",
            "ñ": "n",
        }

        for accented, normal in replacements.items():
            text = text.replace(accented, normal)

        return text
