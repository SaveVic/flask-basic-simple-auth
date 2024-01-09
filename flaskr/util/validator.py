from typing import Union
import re


class Validator:
    def __init__(self, data: dict[str, str]) -> None:
        self.__data = data
        self.__field = None
        self.__value = None
        self.__msg = None

    def set_field(self, field: str):
        self.__field = field
        self.__value = self.__data[field]
        return self

    def msg(self):
        return self.__msg

    def __combine(self, new_val: Union[str, None]):
        if self.__msg is None:
            self.__msg = new_val
        return self

    def is_not_empty(self):
        value = self.__value
        msg = None
        if not isinstance(value, str) or value is None or value == '':
            msg = f'{str.capitalize(self.__field)} is required!'
        return self.__combine(msg)

    def is_email(self):
        value = self.__value
        msg = None
        if value is None or not re.match(r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$', value):
            msg = f'Invalid email address!'
        return self.__combine(msg)

    def is_alphanumeric(self):
        value = self.__value
        msg = None
        if value is None or not re.fullmatch(r'[A-Za-z0-9]+', value):
            msg = f'{str.capitalize(self.__field)} must contain only characters and numbers!'
        return self.__combine(msg)
