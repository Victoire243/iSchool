"""Configuration de l'application"""


class Config:
    """Configuration principale de l'application"""

    # API Configuration
    API_BASE_URL = "http://127.0.0.1:5000/api"

    # UI Configuration
    APP_TITLE = "iSchool"
    SCHOOL_NAME = "iSchool"

    # Window Configuration
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    MIN_WINDOW_WIDTH = 800
    MIN_WINDOW_HEIGHT = 600

    # Colors
    PRIMARY_COLOR = "#1976D2"  # Blue 700
    SECONDARY_COLOR = "#388E3C"  # Green 700

    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    CLOSE_BANNER_TIME = 3  # in secs

    # -------- Impression / Reçus --------
    # Chemin vers le logo (utilisé dans les PDF et tickets si supporté)
    RECEIPT_LOGO_PATH = "src/assets/icon.png"

    # Format par défaut pour l'impression des reçus ("A4" | "POS" | "ESC_POS")
    DEFAULT_RECEIPT_FORMAT = "A4"

    # Configuration ESC/POS (adapter selon le type de connexion de l'imprimante)
    ESC_POS_CONNECTION_TYPE = "USB"  # "USB" | "NETWORK" | "SERIAL"

    # Si USB: Identifiants Vendor/Product (hexadécimal, souvent fournis par le fabricant)
    ESC_POS_USB_VENDOR_ID = 0x0000  # A REMPLACER
    ESC_POS_USB_PRODUCT_ID = 0x0000  # A REMPLACER
    # Points de terminaison (laisser None si inconnu, la lib essaiera des valeurs par défaut)
    ESC_POS_USB_IN_EP = None
    ESC_POS_USB_OUT_EP = None

    # Si NETWORK: adresse IP et port de l'imprimante (ex: 192.168.1.50:9100)
    ESC_POS_NETWORK_HOST = "192.168.1.50"
    ESC_POS_NETWORK_PORT = 9100

    # Si SERIAL: port et baudrate (ex: COM3 sous Windows, /dev/ttyUSB0 sous Linux)
    ESC_POS_SERIAL_PORT = "COM3"
    ESC_POS_SERIAL_BAUDRATE = 19200

    # Largeur des caractères (colonnes) pour ticket texte simple
    POS_TICKET_WIDTH = 40
