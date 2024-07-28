# flake8: noqa
from modules.database.schemas import message_schemas

base_responses = {
    400: {
        "model": message_schemas.Message,
        "description": "Bad Request",
        "example": {"detail": "The request was unacceptable, often to due missing a required parameter."},
    },
    401: {
        "model": message_schemas.Message,
        "description": "Unauthorized",
        "example": {"detail": "Could not validate credentials (no valid API key provided)."},
    },
    403: {
        "model": message_schemas.Message,
        "description": "Forbidden",
        "example": {"detail": "The API key used doesn't have permissions to perform the request."},
    },
    404: {
        "model": message_schemas.Message,
        "description": "Resource Not Found",
        "example": {"detail": "The requested resource doesn't exist."},
    },
    500: {
        "model": message_schemas.Message,
        "description": "Internal Server Error",
        "example": {"detail": "Something went wrong on Reboot Motion's end (these are rare)."},
    },
}
