class UsageError(Exception):
    """Raised when a command receives wrong arguments."""


class NotFoundError(ValueError):
    """Raised when a requested entity does not exist."""


class AlreadyExistsError(ValueError):
    """Raised when an entity that should be unique already exists."""
