# python version 3.8
# UTF-8 encoding
import codecs
import datetime
import re
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

        # Smart line breaks: add line breaks with a substitude; ie. "  " (two spaces)
        self.smart_line_break = True
        self.line_break_pattern = "\s\s"
        self.line_break_char = "\n"

        # Cleanup spaces (double, leading, and trailing)
        self.cleanup_spaces = True

        # Add priority tags to entry
        self.use_priority_tags = True
        self.priority_tag = '#'  # tag that marks a priority value: #B => [#B]

        # Add a task created date to entry
        self.add_creation_date = True  # add a creation date to the entry
        self.creation_date_format = ":PROPERTIES:\n:CREATED: [%s-%s-%s %s]\n:END:"

        # Replace absolute dates like 01.10 15:00 => <2016-10-01 Sun 15:00>
        self.replace_absolute_dates = True

        # Replace relative dates
        self.replace_relative_dates = True
        self.date_format = "<%s-%s-%s %s>"
        self.date_format_regex = "<\d{4}-\d{2}-\d{2}\s[A-Z][a-z]{2}>"
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

        # Schedule and deadline keywords
        self.convert_deadlines = True
        self.deadline_pattern = "DL: "
        self.deadline_keyword = "DEADLINE: "

        self.convert_scheduled = True
        self.scheduled_pattern = "S: "
        self.scheduled_keyword = "SCHEDULED: "

        # Message handling
        self.message_format = [
            "Added '%s' to %s.",  # input without body
            "Added '%s\n%s' to %s."  # input with heading and body
        ]

    def encode(self, string):
        """Encode the input string into unicode."""
        # if not isinstance(string, unicode):
        #     string = unicode(string, "utf-8")
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
        deadline, scheduled = None, None

        # Format body
        if len(items) == 1:
            # String has no body
            body = ""
            self.body = None
        else:
            # String has a body
            body = items[1]

            if self.replace_absolute_dates is True:
                # Replace absolute dates
                body = self.convert_absolute_date(body)

            if self.replace_relative_dates is True:
                # Replace relative dates
                body = self.replace_date(body)

            if self.smart_line_break is True:
                # convert line breaks
                body = self.convert_line_breaks(body)

            if self.convert_deadlines is True:
                # Replace deadlines
                deadline, body = self.get_deadline_date(body)

            if self.convert_scheduled is True:
                # Replace deadlines
                scheduled, body = self.get_scheduled_date(body)

            if self.cleanup_spaces is True:
                body = self.remove_double_spaces(body)
                body = self.remove_leading_trailling_spaces(body)

            self.body = body

        # Format heading
        heading = items[0]
        # Priority
        if self.use_priority_tags is True:
            # Search heading string for priority tag and add an orgmode
            # priority tag to the heading
            heading = self.add_priority(heading)

        self.heading = heading
        heading = self.heading_suffix + heading

        # Format entry
        entry = heading
        if deadline is not None:
            entry += '\n%s' % deadline
        if scheduled is not None:
            if deadline is not None:
                entry += ' '
            else:
                entry += '\n'
            entry += scheduled
        if self.add_creation_date is True:
            entry += '\n%s' % self.get_creation_date()
        entry += '\n%s' % body

        return entry

    def split_string(self, string):
        return string.split(self.delimiter)

    def replace_date(self, string):
        dict_keys = '|'.join(self.weekdays.keys()) + "|" + '|'.join(
            self.relative_dates.keys())
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

    def convert_absolute_date(self, string):
        # Set up pattern
        date_pattern = [
            '\d{1,2}\.\d{1,2}\.\d{4}',  # 01.09.2016 and 1.9.2016
            '\d{1,2}\.\d{1,2}'
        ]
        time_pattern = '\s\d{2}\:\d{2}'  # HH:MM

        # Search for date string
        date = None
        # Pattern 0
        pattern = "(%s)" % date_pattern[0]
        result = re.search(pattern, string)
        # format to orgmode timestamp
        if result is not None:
            sub_pattern = pattern
            date = result.group(1)
            date = datetime.datetime.strptime(
                date, '%d.%m.%Y').strftime('%Y-%m-%d %a')
            # format as orgmode date format
            # date = self.format_date(date, self.date_format)
        else:
            # Pattern 1
            pattern = "(%s)" % date_pattern[1]
            result = re.search(pattern, string)
            if result is not None:
                sub_pattern = pattern
                date = result.group(1)
                date = datetime.datetime.strptime(date,
                                                  '%d.%m').strftime('%m-%d')

                # Add year to date
                # Compare with today's date
                today = datetime.datetime.today()
                date_compare = "%s-%s" % (today.year, date)
                date_compare = datetime.datetime.strptime(
                    date_compare, "%Y-%m-%d")
                if date_compare > today:
                    # Date is this year
                    year = today.year
                else:
                    # Date is next year
                    year = today.year + 1
                # Add year to date
                date = "%s-%s" % (year, date)
                # format as orgmode date
                date = datetime.datetime.strptime(
                    date, '%Y-%m-%d').strftime('%Y-%m-%d %a')

        # Search for time in string
        time = ""
        pattern = "(%s|%s)(%s)" % (date_pattern[0], date_pattern[1],
                                   time_pattern)
        result = re.search(pattern, string)
        if result is not None:
            sub_pattern = pattern
            time = result.group(2)

        if date is not None:
            # format as orgmode timestamp
            date = "<%s%s>" % (date, time)

            # replace date with orgmode timestamp
            string = re.sub(sub_pattern, date, string, count=1)

        return string

    def get_creation_date(self):
        today = datetime.datetime.now()
        date = self.format_date(today, self.creation_date_format)
        return date

    def add_priority(self, heading):
        # search for priority tag
        pattern = '(.+?|.?)%s(.?)\s' % self.priority_tag
        result = re.match(pattern, heading)

        # Add orgmode's priority tag to heading
        if result is not None:
            # remove priority tag from heading
            pattern = '(%s.?)\s' % self.priority_tag
            heading = re.sub(pattern, "", heading)

            # add priority to heading
            priority = result.group(2).upper()
            task_tag = "TODO"
            if re.match(task_tag, heading) is not None:
                # Heading is task: add priority after task tag
                task_tag_pos = len(task_tag)
                heading = "%s [#%s] %s" % (heading[:task_tag_pos], priority,
                                           heading[task_tag_pos + 1:])
            else:
                # Heading is note
                heading = "[#%s] %s" % (priority, heading)
        return heading

    def convert_line_breaks(self, string):
        expression = r'(' + self.line_break_pattern + ')'
        pattern = re.compile(expression, re.IGNORECASE)
        string = re.sub(pattern, self.line_break_char, string)
        return string

    def remove_double_spaces(self, string):
        # remove double spaces (run twice)
        expression = r'(' + '\s\s' + ')'
        pattern = re.compile(expression)
        for i in range(2):
            string = re.sub(pattern, ' ', string)
        return string

    def remove_leading_trailling_spaces(self, string):
        # remove leading and trailing spaces
        expression = r'(' + '^\s|\s$' ')'
        pattern = re.compile(expression)
        string = re.sub(pattern, '', string)
        return string

    def get_deadline_date(self, string):
        # Get deadline
        expression = r'(' + self.deadline_pattern + self.date_format_regex + ')'
        pattern = re.compile(expression, re.IGNORECASE)
        deadline = re.search(pattern, string)
        if deadline is not None:
            # DL: => DEADLINE:
            deadline = re.sub(r'(' + self.deadline_pattern + ')',
                              self.deadline_keyword, deadline.group(1))

        # Remove deadline from string
        pattern = re.compile(expression, re.IGNORECASE)
        body = re.sub(pattern, '', string)

        return deadline, body

    def get_scheduled_date(self, string):
        # Get scheduled
        expression = r'(' + self.scheduled_pattern + self.date_format_regex + ')'
        pattern = re.compile(expression, re.IGNORECASE)
        scheduled = re.search(pattern, string)
        if scheduled is not None:
            # S: => SCHEDULED:
            scheduled = re.sub(r'(' + self.scheduled_pattern + ')',
                               self.scheduled_keyword, scheduled.group(1))

        # Remove scheduled from string
        pattern = re.compile(expression, re.IGNORECASE)
        body = re.sub(pattern, '', string)

        return scheduled, body

    def create_message(self):
        # Get inbox_file of file path
        filepath = self.inbox_file.split('/')
        filename = filepath[len(filepath) - 1]

        if self.body is None:
            message = self.message_format[0] % (self.heading, filename)
        else:
            message = self.message_format[1] % (self.heading, self.body,
                                                filename)

        return message
