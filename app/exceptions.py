from fastapi import HTTPException

def not_found(message: str = "Resource not found") -> HTTPException:
    """
    Raises a 404 Not Found HTTP exception with the provided message.
    """
    return HTTPException(status_code=404, detail=message)

def unauthorized(message: str = "Unauthorized") -> HTTPException:
    """
    Raises a 401 Unauthorized HTTP exception with the provided message.
    """
    return HTTPException(status_code=401, detail=message)

def forbidden(message: str = "Forbidden") -> HTTPException:
    """
    Raises a 403 Forbidden HTTP exception with the provided message.
    """
    return HTTPException(status_code=403, detail=message)

def internal_server_error(message: str = "Internal Server Error") -> HTTPException:
    """
    Raises a 500 Internal Server Error HTTP exception with the provided message.
    """
    return HTTPException(status_code=500, detail=message)

def bad_request(message: str = "Bad Request") -> HTTPException:
    """
    Raises a 400 Bad Request HTTP exception with the provided message.
    """
    return HTTPException(status_code=400, detail=message)