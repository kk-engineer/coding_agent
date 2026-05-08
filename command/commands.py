from enum import Enum


class Command(str, Enum):

    HELP = "/help"

    EDIT = "/edit"

    PLAN = "/plan"

    EXPLAIN = "/explain"

    SEARCH = "/search"

    TEST = "/test"

    EXIT = "/exit"