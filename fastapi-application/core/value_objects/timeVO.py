from dataclasses import dataclass


@dataclass
class TimeVO:
    def __init__(self, seconds: int):
        self.seconds = seconds

    @property
    def second(self):
        return self.seconds

    @property
    def minute(self):
        return self.seconds // 60

    def __composite_values__(self):
        return (self.seconds,)

    def __repr__(self):
        return f"<TimeVO {self.minute} мин.>"

    def __eq__(self, other):
        return isinstance(other, TimeVO) and self.seconds == other.seconds
