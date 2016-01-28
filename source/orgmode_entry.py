# python version 2.7
import datetime
import re
# UTF-8 encoding
import codecs
import unicodedata


class OrgmodeEntry(object):
    """Convert a generic text into an org-mode heading with an optional body and add it to an orgmode file.

    Supported modes:
        - convert relative dates like Thuesday, tomorrow, morgen and montag into org-mode dates
        - add the date of creation to the heading
    """
    def __init__(self):
        self.inbox_file = "/Users/Alex/Desktop/inbox.org"
        self.delimiter = ":: "

        # Depth of heading
        self.heading_suffix = "\n* "

        # Creation date handling
        self.add_creation_date = False  # add a creation date to the entry
        self.creation_date_format = ":PROPERTIES:\n:Created: [%s-%s-%s %s]\n:END:"

        # Relative date handling
        self.replace_relative_dates = True  # set to False to disable replacement of relative dates
        self.date_format = "<%s-%s-%s %s>"
        self.weekdays = {
            "montag": 0,
            "monday": 0,
            "dienstag": 1,
            "tuesday": 1,
            "mittwoch": 2,
            "wednesday": 2,
            "donnerstag": 3,
            "thursday": 3,
            "freitag": 4,
            "friday": 4,
            "samstag": 5,
            "saturday": 5,
            "sonntag": 6,
            "sunday": 6
        }
        self.relative_dates = {
            "heute": 0,
            "today": 0,
            "morgen": 1,
            "tomorrow": 1
        }
        self.convenience_dates = []
        for month in range(1, 13):
            for day in range(1, 32):
                date = "%s.%s" % (day, month)
                self.convenience_dates.append(date)

        # Special characters
        # Smart line breaks: add line breaks with a substitude; ie. "  " (two spaces)
        self.smart_line_break = True
        self.line_break_pattern = "\s\s"
        self.line_break_char = "\n"

        # Message handling
        self.message_format = [
            "Added '%s' to %s.",  # input without body
            "Added '%s\n%s' to %s."  # input with heading and body
        ]

    def encode(self, string):
        """Encode the input string into unicode."""
        if not isinstance(string, unicode):
            string = unicode(string, "utf-8")
        string = unicodedata.normalize('NFC', string)
        return string

    def add_entry(self, string):
        string = self.encode(string)
        entry = self.format_entry(string)
        self.write_to_file(entry)
        message = self.create_message()
        return message

    def write_to_file(self, string):
        with codecs.open(self.inbox_file, "a", encoding='utf-8') as myfile:
            myfile.write(string)
        pass

    def format_entry(self, string):
        items = self.split_string(string)

        # Format body
        if len(items) == 1:
            # String has no body
            body = ""
            self.body = None
        else:
            # String has a body
            body = items[1]

            if self.replace_relative_dates is True:
                # Replace relative dates
                body = self.replace_date(body)

            if self.smart_line_break is True:
                # convert line breaks
                body = self.convert_line_breaks(body)

            self.body = body
            body = "\n" + body

        # Format heading
        heading = items[0]
        self.heading = heading
        heading = self.heading_suffix + heading

        # Format entry
        entry = heading + self.get_creation_date() + body

        return entry

    def split_string(self, string):
        return string.split(self.delimiter)

    def replace_date(self, string):
        dict_keys = '|'.join(self.weekdays.keys()) + "|" + '|'.join(self.relative_dates.keys())
        expression = r'\b(' + dict_keys + r')\b'
        pattern = re.compile(expression, re.IGNORECASE)
        string = pattern.sub(lambda x: self.convert_date(x.group()), string)
        return string

    def convert_date(self, string):
        today = datetime.datetime.now()
        delta = self.convert_relative_date(string)
        date = today + datetime.timedelta(days=delta)
        date = self.format_date(date, self.date_format)
        return date

    def convert_relative_date(self, string):
        # string dictionaries with delta day value
        string = string.lower()
        relative_dates = self.relative_dates
        weekdays = self.weekdays
        convenience_dates = self.convenience_dates

        if string in relative_dates:
            delta = relative_dates[string]
        elif string in weekdays:
            today = datetime.datetime.today()
            current = today.weekday()
            weekday = weekdays[string]
            if current == weekday:
                delta = 7
            elif weekday < current:
                delta = 7 - (current - weekday)
            else:
                delta = weekday - current
        # TODO: Extend replace date function
        elif string in convenience_dates:
            item = string.split(".")
            day = item[0]
            month = item[1]
            print(day, month)
            delta = False
        else:
            delta = False
        return delta

    def format_date(self, date, date_format):
        year = date.strftime("%Y")
        month = date.strftime("%m")
        day = date.strftime("%d")
        weekday = date.strftime("%a")

        date = date_format % (year, month, day, weekday)
        return date

    def get_creation_date(self):
        if self.add_creation_date is True:
            today = datetime.datetime.now()
            date = self.format_date(today, self.creation_date_format)
            date = "\n" + date
            return date
        else:
            return ""

    def convert_line_breaks(self, string):
        expression = r'(' + self.line_break_pattern + ')'
        pattern = re.compile(expression, re.IGNORECASE)
        result = re.sub(pattern, self.line_break_char, string)
        return result

    def create_message(self):
        # Get inbox_file of file path
        filepath = self.inbox_file.split('/')
        filename = filepath[len(filepath) - 1]

        if self.body is None:
            message = self.message_format[0] % (self.heading, filename)
        else:
            message = self.message_format[1] % (self.heading, self.body, filename)

        return message
