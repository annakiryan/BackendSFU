from dataclasses import dataclass


@dataclass
class PriceVO:
    def __init__(self, price_in_coins: int):
        self.price_in_coins = price_in_coins

    @property
    def min_value(self):
        return self.price_in_coins

    @property
    def max_value(self):
        return self.price_in_coins // 100

    @property
    def format(self):
        rub = self.price_in_coins // 100
        kop = self.price_in_coins % 100
        if kop == 0:
            return f"{rub} руб."
        return f"{rub} руб. {kop} коп."

    def __composite_values__(self):
        return (self.price_in_coins,)

    def __repr__(self):
        return f"<PriceVO {self.format}>"

    def __eq__(self, other):
        return (
            isinstance(other, PriceVO) and self.price_in_coins == other.price_in_coins
        )
