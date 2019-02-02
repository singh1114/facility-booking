class ClubHouse:
    """Club house constants."""

    # ('start_time', 'end_time'): hourly_price
    SLOT_MAP = {
        ('10:00', '16:00'): 100,
        ('16:00', '22:00'): 500,
    }


class TennisCourt:
    """Tennis Court constants."""

    HOURLY_PRICE = 50
