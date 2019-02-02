from abc import ABCMeta, abstractmethod

import time
import datetime

from custom_exceptions import (
    CantBookFacility,
    CantBookVariablePricing,
    DateFormatNotValidException,
    TimeFormatNotValidException
)
from constants import ClubHouse, TennisCourt
from utils import get_hour_bucket_from_slot


class BaseBooking(metaclass=ABCMeta):

    def __init__(self, booking_date, start_time, end_time):
        self.booking_date = self.is_date_valid(booking_date)
        self.start_time = self.is_time_valid(start_time)
        self.end_time = self.is_time_valid(end_time)

    @abstractmethod
    def book_facility(self):
        raise NotImplementedError(
            'book_facility method has not been defined in child class.')

    def is_date_valid(self, date):
        try:
            return datetime.datetime.strptime(date, '%Y-%M-%d')
        except ValueError:
            raise DateFormatNotValidException()

    def is_time_valid(self, str_time):
        try:
            return time.strptime(str_time, '%H:%M')
        except ValueError:
            raise TimeFormatNotValidException()


class BookTennisCourt(BaseBooking):

    booking_date = None
    start_time = None
    end_time = None

    def book_facility(self):
        return self.get_total_cost()

    def get_total_cost(self):
        return TennisCourt.HOURLY_PRICE * (
                self.end_time.tm_hour - self.start_time.tm_hour)


class BookClubHouse(BaseBooking):

    def book_facility(self):
        return self.get_total_cost()


    def get_total_cost(self):
        if self.check_constant_pricing():
            start_slot_price, _ = self.get_start_end_slot_prices()
            return start_slot_price * (
                    self.end_time.tm_hour - self.start_time.tm_hour)
        else:
            raise CantBookVariablePricing()

    def check_constant_pricing(self):
        """Check if start_time and end_time both are in one slot."""
        start_slot_price, end_slot_price = self.get_start_end_slot_prices()

        if start_slot_price == end_slot_price and start_slot_price != 0:
            return True

        return False

    def get_start_end_slot_prices(self):
        start_slot_price = 0
        end_slot_price = 0
        for slot, price in ClubHouse.SLOT_MAP.items():
            hour_bucket = get_hour_bucket_from_slot(slot)
            if self.start_time.tm_hour in range(
                    hour_bucket[0], hour_bucket[1] + 1):
                start_slot_price = price
            if self.end_time.tm_hour in range(
                    hour_bucket[0], hour_bucket[1] + 1):
                end_slot_price = price
            if start_slot_price == end_slot_price and start_slot_price != 0:
                break
        return start_slot_price, end_slot_price


class BookFacility:
    club_house_booking_data = []
    tennis_court_booking_data = []

    def can_book_facility(self, facility, date, start_time, end_time):
        data_class = self.get_facility_data_class(facility)
        given_date_booking_data = [data for data in (
            data_class) if data.get('date') == date]
        for data in given_date_booking_data:
            hour_bucket = get_hour_bucket_from_slot((
                data['start_time'].split(':')[0],
                data['end_time'].split(':')[0]))
            if int(start_time.split(':')[0]) in range(
                    hour_bucket[0], hour_bucket[1]
            ) or int(end_time.split(':')[0]) in range(
                hour_bucket[0], hour_bucket[1]
            ):
                return False
        return True

    def book_facility(self, facility, date, start_time, end_time):
        data_class = self.get_facility_data_class(facility)
        if self.can_book_facility(facility, date, start_time, end_time):
            data_class.append({
                'date': date,
                'start_time': start_time,
                'end_time': end_time
            })
            return self.get_total_cost(facility, date, start_time, end_time)
        else:
            raise CantBookFacility()

    def get_facility_data_class(self, facility):
        data_class = None
        if facility == 'Club House':
            data_class = self.club_house_booking_data
        elif facility =='Tennis Court':
            data_class = self.tennis_court_booking_data

        return data_class

    def get_total_cost(self, facility, date, start_time, end_time):
        booking_class = None
        if facility == 'Club House':
            booking_class = BookClubHouse(date, start_time, end_time)
        elif facility =='Tennis Court':
            booking_class = BookTennisCourt(date, start_time, end_time)

        return booking_class.get_total_cost()



