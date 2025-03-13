from typing import Self


class ObjList:
    __slots__ = ("__next", "__prev", "__data")

    def __init__(self, data):
        self.set_data(data)
        self.set_next(None)
        self.set_prev(None)

    def set_next(self, obj: Self):
        self.__next = obj

    def set_prev(self, obj: Self):
        self.__prev = obj

    def set_data(self, data):
        self.__data = data

    def get_next(self) -> Self:
        return self.__next

    def get_prev(self) -> Self:
        return self.__prev

    def get_data(self):
        return self.__data


class LinkedList:
    __slots__ = (
        "head",
        "tail",
    )

    def __init__(self):
        self.head: ObjList = None
        self.tail: ObjList = None

    def add_obj(self, obj: ObjList):
        if not self.head:
            # ? first item in a list
            self.head = obj
            self.tail = obj
        elif not self.tail:
            raise ValueError("no tail in a non-empty list")
        else:
            self.tail.set_next(obj)
            obj.set_prev(self.tail)
            self.tail = obj

    def remove_obj(self):
        if not self.head:
            raise IndexError("remove from empty list")
        if not self.tail:
            raise ValueError("no tail in a non-empty list")

        new_tail = self.tail.get_prev()
        if new_tail:
            # ? there are some elements in a list
            new_tail.set_next(None)
        else:
            # ? no previous elements, list would be empty
            self.head = None

        # ? apply new tail
        self.tail = new_tail

    def get_data(self) -> list:
        current = self.head
        container = []
        while current:
            container.append(current.get_data())
            current = current.get_next()
        return container
