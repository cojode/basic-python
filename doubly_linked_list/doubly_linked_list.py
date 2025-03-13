from typing import Self


class CorruptedLinkedListError(Exception): ...


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

    def _raise_if_corrupted(self):
        if self.head and not self.tail:
            raise CorruptedLinkedListError("no tail in a non-empty list")
        # ? cycle detection could be also introduced here

    def add_obj(self, obj: ObjList):
        """Append an ObjList object to the end of the sequence.

        :param obj: object to add
        :type obj: ObjList
        :raises CorruptedLinkedListError: there is no tail in a sequence currently
        """

        self._raise_if_corrupted()

        if not isinstance(obj, ObjList):
            raise TypeError("obj must be an instance of ObjList")

        if not self.head:
            # ? first item in a list
            self.head = obj
            self.tail = obj
        else:
            self.tail.set_next(obj)
            obj.set_prev(self.tail)
            self.tail = obj

        # ? cycle prevention
        obj.set_next(None)

    def remove_obj(self) -> ObjList:
        """Pops last object from the sequence.

        :raises IndexError: pop from empty list
        :raises CorruptedLinkedListError: there is no tail in a sequence currently
        """
        self._raise_if_corrupted()

        if not self.head:
            raise IndexError("remove from empty list")

        discarded_tail = self.tail

        new_tail = self.tail.get_prev()
        if new_tail:
            # ? there are some elements in a list
            new_tail.set_next(None)
        else:
            # ? no previous elements, list would be empty
            self.head = None

        # ? apply new tail
        self.tail = new_tail

        return discarded_tail

    def get_data(self) -> list:
        """Returns a sequence item's data in a list.

        :return: list of data values
        :rtype: list
        """
        self._raise_if_corrupted()

        current = self.head
        container = []
        while current:
            container.append(current.get_data())
            current = current.get_next()
        return container
