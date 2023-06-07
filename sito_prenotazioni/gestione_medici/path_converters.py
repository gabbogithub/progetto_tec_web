from django.utils.dateparse import parse_datetime

class NameConverter:
    regex = '[a-zA-Z]*'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
    
class DateConverter:
    regex = '([\d]{4}-[\d]{2}-[\d]{2}\s([\d]{2}:){2}[\d]{2}\+[\d]{2}:[\d]{2})\|(None)'

    def to_python(self, value):
        date = None

        try:
            date = parse_datetime(value)
        except:
            pass

        return date
          

    def to_url(self, value):
        date = ''

        try:
            date = value
        except:
            pass

        return date