"""Fichier d'initialisation pour le module models"""

from .user_model import UserModel
from .cash_register_model import CashRegisterModel
from .classroom_model import ClassroomModel
from .enrollment_model import EnrollmentModel
from .expense_model import ExpenseModel
from .payment_model import PaymentModel
from .payment_type_model import PaymentTypeModel
from .fee_model import FeeModel
from .role_model import RoleModel
from .school_year_model import SchoolYearModel
from .staff_model import StaffModel
from .staff_payment_model import StaffPaymentModel
from .student_model import StudentModel


__all__ = [
    "UserModel",
    "CashRegisterModel",
    "ClassroomModel",
    "EnrollmentModel",
    "ExpenseModel",
    "PaymentModel",
    "RoleModel",
    "SchoolYearModel",
    "StaffModel",
    "StaffPaymentModel",
    "StudentModel",
    "PaymentTypeModel",
    "FeeModel",
]
