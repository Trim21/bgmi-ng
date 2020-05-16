"""exceptions"""


class BGmiException(Exception):
    """Base Exception for all BGmi exception"""


class BGmiConnectionException(BGmiException):
    """Base Exception for all connection error"""


class SubscriptionNotFollowed(BGmiException):
    """Subscription not found when lookup"""


class SeriesNotFollowed(BGmiException):
    """Series not found when lookup"""


class RequireNotSatisfiedError(BGmiException):
    """exception when missing config or deps for a output plugin"""

    message: str

    def __init__(self, message: str):
        """init

        :param message: error detail message for user
        """
        self.message = message


class ConnectError(BGmiConnectionException):
    """exception when output get a connection error"""


class AuthError(BGmiException):
    """exception when output require correct auth"""
