class PriceConverter:
    @staticmethod
    def rub_to_coins(rub: int) -> int:
        return rub * 100

    @staticmethod
    def coins_to_rub(coins: int) -> int:
        return coins // 100


class TimeConverter:
    @staticmethod
    def min_to_sec(minutes: int) -> int:
        return minutes * 60

    @staticmethod
    def sec_to_min(seconds: int) -> int:
        return seconds // 60
