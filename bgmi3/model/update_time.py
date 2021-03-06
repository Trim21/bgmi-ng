from enum import Enum


class UpdateTime(str, Enum):
    mon = "Mon"
    tue = "Tue"
    wed = "Wed"
    thu = "Thu"
    fri = "Fri"
    sat = "Sat"
    sun = "Sun"

    def __str__(self) -> str:
        return self.value
