import unittest

from book_facility import BookClubHouse, BookFacility, BookTennisCourt

from custom_exceptions import CantBookFacility

class TestBookFacility(unittest.TestCase):
    def test_tennis_court_booking(self):
        facility = 'Tennis Court'
        date = '2019-01-27'
        start_time = '10:00'
        end_time = '12:00'
        bf = BookFacility()
        self.assertEqual(
            bf.book_facility(facility, date, start_time, end_time),
            BookTennisCourt(date, start_time, end_time).get_total_cost())

        with self.assertRaises(CantBookFacility):
            bf.book_facility(facility, date, start_time, end_time)

        start_time = '12:00'
        end_time = '22:00'
        self.assertEqual(
            bf.book_facility(facility, date, start_time, end_time),
            BookTennisCourt(date, start_time, end_time).get_total_cost())

    def test_club_house_booking(self):
        facility = 'Club House'
        date = '2019-01-27'
        start_time = '10:00'
        end_time = '16:00'
        bf = BookFacility()
        self.assertEqual(
            bf.book_facility(facility, date, start_time, end_time),
            BookClubHouse(date, start_time, end_time).get_total_cost())

        with self.assertRaises(CantBookFacility):
            bf.book_facility(facility, date, start_time, end_time)

        start_time = '16:00'
        end_time = '22:00'
        self.assertEqual(
            bf.book_facility(facility, date, start_time, end_time),
            BookClubHouse(date, start_time, end_time).get_total_cost())
