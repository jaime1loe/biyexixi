"""
自定义异常处理
"""

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from sqlalchemy.exc import SQLAlchemyError


async def sqlalchemy_exception_handler(_request: Request, exc: SQLAlchemyError):
    """处理SQLAlchemy数据库异常"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "数据库操作失败",
            "error": str(exc)
        }
    )


async def http_exception_handler(_request: Request, exc: HTTPException):
    """处理HTTP异常"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "code": exc.status_code
        }
    )


def validation_exception_handler(_request: Request, exc: RequestValidationError):
    """处理请求验证异常"""
    errors: list[dict[str, str]] = []
    for error in exc.errors():  # type: ignore
        # type: ignore
        error_loc = error["loc"]  # type: ignore
        error_msg = error["msg"]  # type: ignore
        error_type = error["type"]  # type: ignore

        errors.append({
            "field": ".".join(str(loc) for loc in error_loc),  # type: ignore
            "message": error_msg,
            "type": error_type
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "请求参数验证失败",
            "errors": errors
        }
    )


class ServiceException(Exception):
    """业务异常基类"""
    message: str
    code: int

    def __init__(self, message: str, code: int = 400) -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)


class BadRequestException(ServiceException):
    """400错误"""
    def __init__(self, message: str = "请求参数错误"):
        super().__init__(message, 400)


class UnauthorizedException(ServiceException):
    """401错误"""
    def __init__(self, message: str = "未授权访问"):
        super().__init__(message, 401)


class ForbiddenException(ServiceException):
    """403错误"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(message, 403)


class NotFoundException(ServiceException):
    """404错误"""
    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, 404)


class ConflictException(ServiceException):
    """409错误"""
    def __init__(self, message: str = "资源冲突"):
        super().__init__(message, 409)
