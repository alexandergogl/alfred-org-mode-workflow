# coding=utf-8

from orgmode_entry import OrgmodeEntry

entry = u'#A Etwas machen:: DL: Morgen S: Heute Ausstellung am 23.09.2014 12:00 oder am Montag   bzw. am 22.10 13:00 sollte man anschauen. '

org = OrgmodeEntry()
# Use an absolute path
org.inbox_file = '/Users/Alex/Documents/Planung/Planning/Inbox.org'

org.delimiter = ':: '  # tag to separate the head from the body of the entry
org.heading_suffix = "\n* "  # depth of entry

org.use_priority_tags = True  # use priority tags: #b => [#B]
org.priority_tag = '#'  # tag that marks a priority value

org.add_creation_date = True  # add a creation date

org.replace_absolute_dates = True  # convert absolute dates like 01.10 15:00 into orgmode dates => <2016-10-01 Sun 15:00>
org.replace_relative_dates = True  # convert relative dates like monday or tomorrow into orgmode dates

# Convert a schedule pattern into an org scheduled date
org.convert_scheduled = True  # convert sche
org.scheduled_pattern = "S: "

# Convert a deadline pattern into an org deadline
org.convert_deadlines = True
org.deadline_pattern = "DL: "

org.smart_line_break = True  # convert a pattern into a linebreak
org.line_break_pattern = "\s\s"  # two spaces

# Cleanup spaces (double, leading, and trailing)
org.cleanup_spaces = True

entry = 'TODO ' + entry

message = org.add_entry(entry).encode('utf-8')

print(message)
