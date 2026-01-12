from fastapi import HTTPException, status


class VocabularyNotFoundError(HTTPException):
    def __init__(self, vocabulary_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vocabulary item with id {vocabulary_id} not found"
        )


class UserNotFoundError(HTTPException):
    def __init__(self, user_id: str = None):
        detail = "User not found"
        if user_id:
            detail = f"User with id {user_id} not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class UnauthorizedError(HTTPException):
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenError(HTTPException):
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class ValidationError(HTTPException):
    def __init__(self, detail: str, field: str = None):
        error_detail = {"detail": detail}
        if field:
            error_detail["field"] = field
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error_detail
        )

