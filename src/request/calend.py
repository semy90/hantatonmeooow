import calendar
import datetime


class Calend:
    def __init__(self):
        self.date = datetime.datetime.now()
        self.year = self.date.year
        self.month = self.date.month
        self.ram_calendar = calendar.Calendar(firstweekday=0).monthdatescalendar(self.year, self.month)

    def left(self):
        self.date -= datetime.timedelta(days=30)
        self._update()

    def right(self):
        self.date += datetime.timedelta(days=30)
        self._update()

    def _update(self):
        self.year = self.date.year
        self.month = self.date.month
        self.ram_calendar = calendar.Calendar(firstweekday=0).monthdatescalendar(self.year, self.month)

    def get(self) -> list[list[datetime]]:
        return self.ram_calendar.copy()
