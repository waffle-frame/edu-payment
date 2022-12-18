from typing import List
from _collections_abc import dict_keys
from aiogram.types import KeyboardButton

def list_to_buttons(list_: List | dict_keys, count: int = 2) -> List[List[KeyboardButton]]:
    """
        ### Dynamic text splitting for buttons
        The `count` argument is responsible for the number of buttons in one row
    """

    temp_list = []
    splitted_list = []

    for i in list_:
        if temp_list.__len__() == count:
            splitted_list.append(temp_list)
            temp_list = []

        temp_list.append(KeyboardButton(i))

    if temp_list != []:
        splitted_list.append(temp_list)

    return splitted_list
