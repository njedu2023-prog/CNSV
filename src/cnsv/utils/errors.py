class CNSVError(Exception):
    """Base exception for CNSV V1.0."""


class DownstreamGateError(CNSVError):
    """Raised when CNSVdata gate blocks downstream use."""
