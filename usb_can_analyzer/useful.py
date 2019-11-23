#!/usr/bin/env python3
# coding: utf-8


from typing import Union


class ImplementError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message


def getNbByte(number: Union[int, str, bytes]) -> int:
    if type(number) == int:					# If number is an int-object, we use the format function to get the associated str-object with hexadecimal digits.
        number = format(number, "x")
    if type(number) == str:					# If number is a str-object, we use the fromhex method from bytes class to get the bytes-object coded in hexadecimal.
        if(len(number) % 2 == 1):				# If the number of digits is odd, we must add ourself a 0 digit at the beginning to have an even number of digit for the bytes.fromhex() method.
            number = "0" + number
        number = bytes.fromhex(number)
    if type(number) != bytes:				# We check that number is a bytes-object.
        raise TypeError("number must be an 'int', a 'bytes' encode with hexadecimal value or a 'str' with hexadecimal digits. number: " + str(number))
    return(len(number))						# The function len() gives us the number of bytes.


if __name__ == "__main__":
    try:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        pass
