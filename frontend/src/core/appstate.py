"""État global de l'application"""

import asyncio

import flet as ft
from data.api.fake_client import FakeApiClient
from typing import Callable, Awaitable
from models.user_model import UserModel


class AppState:
    """État global de l'application"""

    def __init__(self, show_notifications: Callable | Awaitable | None = None):
        self.api_client: FakeApiClient = FakeApiClient()
        self.current_user: UserModel | None = None
        self.current_user_role: str | None = None
        self.current_page: str = "login"
        self.theme_mode: ft.ThemeMode = ft.ThemeMode.LIGHT
        self.notifications: list = []
        self._show_notifications: Callable | Awaitable | None = show_notifications
        self.current_school_year_id: int | None = None
        self.current_school_year_name: str | None = None
        self.current_language: str = "fr"
        self.translations: dict = self.load_translations(self.current_language)
        self.is_logged_in: bool = False

    def is_authenticated(self):
        """Vérifier si l'utilisateur est connecté"""
        return self.current_user is not None

    def close_connexion(self):
        self.current_user = None
        self.current_user_role = None
        self.current_school_year_name = None
        self.current_school_year_id = None
        try:
            asyncio.create_task(self.api_client.close())
        except Exception as e:
            print(f"Erreur lors de la fermeture de la connexion : {e}")

    async def get_user_role(self):
        """Obtenir le rôle de l'utilisateur"""
        if not self.is_authenticated():
            return None
        if self.api_client and self.current_user:
            role = await self.api_client.get_user_role(self.current_user.id_user)
            self.current_user_role = role.role_name if role else None
        return self.current_user_role

    def load_translations(self, language: str) -> dict:
        """Changer la langue de l'application"""
        try:
            import json

            with open(f"langs/{language}.json") as f:
                translations = f.read()
                self.translations = json.loads(translations)
                return json.loads(translations)
        except FileNotFoundError:
            print(f"Le fichier de traduction pour '{language}' n'a pas été trouvé.")
            return {}
        # return {}

    # def has_permission(self, permission: str):
    #     """Vérifier si l'utilisateur a une permission spécifique"""
    #     if not self.is_authenticated():
    #         return False

    #     user_role = self.current_user.get("role")

    #     # Mapping des rôles aux permissions
    #     role_permissions = {
    #         "administrateur": [
    #             "view_eleves",
    #             "create_eleve",
    #             "edit_eleve",
    #             "delete_eleve",
    #             "view_paiements",
    #             "create_paiement",
    #             "edit_paiement",
    #             "process_paiement",
    #             "view_caisse",
    #             "manage_caisse",
    #             "view_rapports",
    #             "export_rapports",
    #             "admin",
    #             "manage_users",
    #         ],
    #         "percepteur": [
    #             "view_eleves",
    #             "view_paiements",
    #             "create_paiement",
    #             "edit_paiement",
    #             "process_paiement",
    #             "view_caisse",
    #             "manage_caisse",
    #             "view_rapports",
    #             "export_rapports",
    #         ],
    #         "directeur": [
    #             "view_eleves",
    #             "create_eleve",
    #             "edit_eleve",
    #             "delete_eleve",
    #             "view_rapports",
    #             "export_rapports",
    #         ],
    #     }

    #     allowed_permissions = role_permissions.get(user_role, [])
    #     return permission in allowed_permissions

    # async def add_notification(self, message: str, type: str = "info"):
    #     """Ajouter une notification"""
    #     self.notifications.append(
    #         {"message": message, "type": type, "timestamp": datetime.now()}
    #     )
    #     if self._show_notifications:
    #         await self._show_notifications(None)

    # def clear_notifications(self):
    #     """Effacer toutes les notifications"""
    #     self.notifications.clear()

    # def logout(self):
    #     """Déconnecter l'utilisateur"""
    #     self.current_user = None
    #     self.api_client.token = None
    #     self.current_page = "login"
    #     self.clear_notifications()

    # def __str__(self):
    #     return f"AppState(current_user={self.current_user}, current_page={self.current_page}, theme_mode={self.theme_mode})"
