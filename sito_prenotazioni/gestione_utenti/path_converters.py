
class EmptyStringConverter:
    """ Definisce un convertitore di argomenti url per una stringa anche vuota """

    regex = '[^/]*'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value