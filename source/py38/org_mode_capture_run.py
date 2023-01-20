import os

from org_mode_entry import OrgmodeEntry


def convert_boolean(string):
    if string == "1":
        return True
    else:
        return False


def run(entry, action):
    org = OrgmodeEntry()

    if action == "note":
        # Entries are added to the following orgmode file (use an absolute path):
        org.inbox_file = os.getenv("notes_inbox")
        # heading level of entry
        org.heading_suffix = "\n%s " % ("*" *
                                        int(os.getenv("notes_heading_level")))
    elif action == "inspiration":
        # Entries are added to the following orgmode file (use an absolute path):
        org.inbox_file = os.getenv("inspirations_inbox")
        # heading level of entry
        org.heading_suffix = "\n%s " % (
            "*" * int(os.getenv("inspirations_heading_level")))
    else:
        # Entry is a todo
        # Entries are added to the following orgmode file (use an absolute path):
        org.inbox_file = os.getenv("todos_inbox")
        # heading level of entry
        org.heading_suffix = "\n%s " % ("*" *
                                        int(os.getenv("todos_heading_level")))

    # tag to separate the head from the body of the entry
    org.delimiter = str(os.getenv("delimiter"))

    # use priority tags: #b => [#B]
    org.use_priority_tags = convert_boolean(os.getenv("use_priority_tags"))
    # tag that marks a priority value
    # Default: #
    org.priority_tag = str(os.getenv("priority_tag"))

    # add a creation date
    org.add_creation_date = convert_boolean(os.getenv("add_creation_date"))

    # convert absolute dates like 01.10 15:00 into orgmode dates => <2016-10-01 Sun 15:00>
    org.replace_absolute_dates = convert_boolean(
        os.getenv("replace_absolute_dates"))

    # convert relative dates like monday or tomorrow into orgmode dates
    org.replace_relative_dates = convert_boolean(
        os.getenv("replace_relative_dates"))

    # Convert a schedule pattern into an org scheduled date
    # Default: "S: "
    org.convert_scheduled = convert_boolean(os.getenv("convert_scheduled"))
    org.scheduled_pattern = str(os.getenv("scheduled_pattern"))

    # Convert a deadline pattern into an org deadline
    # Default: "DL: "
    org.convert_deadlines = convert_boolean(os.getenv("convert_deadlines"))
    org.deadline_pattern = str(os.getenv("deadline_pattern"))

    # convert a pattern into a linebreak
    org.smart_line_break = convert_boolean(os.getenv("smart_line_break"))
    # two spaces
    # Default: "\s\s"
    org.line_break_pattern = os.getenv("line_break_pattern")

    # Cleanup spaces (double, leading, and trailing)
    org.cleanup_spaces = convert_boolean(os.getenv("cleanup_spaces"))

    entry = 'TODO ' + entry
    message = org.add_entry(entry)

    return message
