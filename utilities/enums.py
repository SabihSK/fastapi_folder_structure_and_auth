import enum


class UserRole(enum.Enum):
    """Enum class.

    Args:
        enum (User Role): To check the role of user.
    """

    VENDOR = "vendor"
    USER = "user"


class EmailTemplate(enum.Enum):
    """Enum class.

    Args:
        enum (Email Template): The list of Email Template.
    """

    REGISTER = "register_email_template"
    LOGIN = "login_email_template"
    FORGET_PASS = "forget_pass_email_template"
    DOC_APPROVE = "document_approve"
    DOC_REJECT = "document_reject"
