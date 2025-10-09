# API de développement iSchool (données fictives)

Ce dossier fournit une API locale fictive alimentée par SQLite et générée avec [Faker](https://faker.readthedocs.io/) pour faciliter les tests et le prototypage de l'application iSchool sans dépendre d'un backend réel.

## 🧰 Prérequis

- Python 3.10 ou supérieur (le projet est configuré pour Python 3.13 via l'environnement virtuel `.venv` à la racine du dépôt)
- L'environnement virtuel activé
- Les dépendances Flet, Faker, SQLAlchemy et AioSQLite (déclarées dans `pyproject.toml`)

## 🚀 Mise en route rapide

```powershell
# Depuis la racine du monorepo
& .\.venv\Scripts\Activate.ps1
pip install -e frontend
# ou, pour une installation minimale
pip install faker sqlalchemy aiosqlite flet==0.70.0.dev5623
```

## 🗃️ Génération de données

Le module `data/fake/fake_data.py` contient la fabrique `FakeDataFactory` capable de générer un jeu de données complet conforme aux modèles du dossier `models/`. L'appel utilitaire `initialize_fake_database()` reconstruit une base SQLite (`data/fake/fake_api.db`) en appliquant le schéma et en insérant les données factices.

```python
from frontend.data.fake.fake_data import initialize_fake_database

# Recrée la base et charge des données cohérentes
initialize_fake_database(seed=42)
```

> 💡 Le paramètre `seed` est optionnel : fournissez un entier pour reproduire exactement le même jeu de données à chaque exécution.

## 🌐 Client d'API fictive

`data/api/fake_client.py` expose `FakeApiClient`, une couche d'accès orientée "endpoints" qui encapsule la base SQLite et renvoie des instances des modèles métiers. Les méthodes publiques sont asynchrones : instanciez simplement la classe puis invoquez-les avec `await`.

```python
import asyncio

from frontend.data.api.fake_client import FakeApiClient


async def main() -> None:
    client = FakeApiClient(seed=123)
    resume = await client.get_dashboard_summary()
    premier_eleve = (await client.list_students())[0]
    paiements = await client.list_payments_by_student(premier_eleve.id_student)

    print(resume)
    print(premier_eleve.to_dict())
    print(len(paiements))

    await client.close()


asyncio.run(main())
```

### Principales méthodes disponibles

| Domaine | Méthodes asynchrones clés |
| --- | --- |
| Utilisateurs & rôles | `await list_roles()`, `await list_users()`, `await get_user(id)` |
| Années scolaires | `await list_school_years()`, `await get_active_school_year()` |
| Classes & inscriptions | `await list_classrooms()`, `await list_students()`, `await list_enrollments()`, `await list_enrollments_by_student(id)` |
| Paiements élèves | `await list_payment_types()`, `await list_payments()`, `await list_payments_by_student(id)` |
| Dépenses & staff | `await list_expenses()`, `await list_staff()`, `await list_staff_payments()`, `await list_staff_payments_by_staff(id)` |
| Trésorerie & synthèses | `await list_cash_register_entries()`, `await get_dashboard_summary()`, `await get_student_financial_statement(id)` |

Toutes les méthodes retournent des objets de modèles (`StudentModel`, `PaymentModel`, etc.) déjà disponibles dans `frontend/models/`.

## 🔄 Réinitialiser ou personnaliser les données

- `await client.reset(seed=...)` permet de régénérer la base sans quitter le contexte Python.
- Vous pouvez modifier les règles de génération directement dans `FakeDataFactory` (par exemple le nombre d'élèves, les montants, les statuts, etc.).
- La base SQLite est accessible dans `data/fake/fake_api.db`. Supprimez-la simplement pour forcer une régénération lors du prochain lancement du client.

## 📝 Notes diverses

- Faker est configuré avec la locale `fr_FR` pour produire des noms et adresses francophones.
- Si les caractères accentués s'affichent mal dans un terminal Windows, exécutez `chcp 65001` avant vos scripts pour passer la console en UTF-8.
- Les dépendances principales sont déjà listées dans `pyproject.toml`; pensez à exécuter `pip install -e frontend` après chaque modification importante pour les synchroniser avec votre environnement.
