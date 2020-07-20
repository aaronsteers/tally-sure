"""Functions and classes for uniqueness certification."""

import uuid as _uuid


def uuid():
    """Return a unique GUID."""
    return _uuid.uuid4()


class Unique(object):
    """Base class for classes requiring uniqueness."""

    uuid: str = uuid()

    def __init__(self, uuid: str = None):
        """Initialize.

        Parameters
        ----------
        uuid : str, optional
            Optional UUID override. Otherwise will be generated as a new UUID.
        """
        if uuid:
            self.uuid = uuid

