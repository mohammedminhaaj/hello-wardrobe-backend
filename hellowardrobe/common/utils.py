from rest_framework import status
from common import constants
from rest_framework.response import Response


class ResponsePayload():
    __status = ""
    __message = ""
    __data = None
    __error = None

    def __get_error_dict(self, status_code: int, error_message: str, serializer_error: dict | None = None):
        error_dict = {"code": status_code, "message": error_message}
        if serializer_error:
            error_dict.update({"errors": serializer_error})
        return error_dict

    def __base_error(self):
        self.__status = "error"
        self.__message = constants.DEFAULT_ERROR

    def as_json(self):
        return {"status": self.__status, "message": self.__message, "data": self.__data, "error": self.__error}

    def success(self, success_message: str | None = constants.SUCCESS, data: dict | None = None):
        self.__status = "success"
        self.__message = success_message
        if not isinstance(data, dict):
            raise ValueError(
                "Invalid data type passed to data. Please use a dictionary")
        self.__data = data
        return Response(self.as_json(), status=status.HTTP_200_OK)

    def error(self, error_message: str | None = constants.DEFAULT_ERROR, status_code: int | None = status.HTTP_400_BAD_REQUEST):
        self.__base_error()
        self.__error = self.__get_error_dict(status_code, error_message)
        return Response(self.as_json(), status=status_code)

    def serializer_error(self, serializer_error: dict, error_message: str | None = constants.FIX_ERRORS, status_code: int | None = status.HTTP_400_BAD_REQUEST):
        self.__base_error()
        self.__error = self.__get_error_dict(
            status_code, error_message, serializer_error)
        return Response(self.as_json(), status=status_code)

    def __str__(self) -> str:
        return f"{self.__status} - {self.__message}"

    def __repr__(self) -> str:
        return str(self.as_json())

    def __dict__(self) -> dict:
        return self.as_json()
