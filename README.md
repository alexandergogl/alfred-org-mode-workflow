# An org-mode-capture workflow for Alfred
Append a todo or a note to an org-mode file with a short and convenient command in [Alfred](https://www.alfredapp.com/). The workflow requires Alfred's "Powerpack."

## Features
The command appends a second level heading to a user defined .org file and puts all what follows `:: ` into the body of the heading (see figures below).

Type todo to add a todo:

![Capture a todo](images/todo-capture.png)

![Capture a todo](images/todo-notification.png)


Type note to add a note:

![Capture a note](images/note-capture.png)

![Capture a note](images/note-notification.png)


The added notes and todos are divided into title and content:

![Capture a note](images/result.png)


Relative dates (Monday, tuesday, tomorrow, morgen, freitag) in the content part of the entry are converted into orgmode specific date formats `<2015-09-11 Fri>`.

![Relative dates in Alfred](images/date_replacement-01.png)

![become orgmode dates](images/date_replacement-02.png)


If enabled, then date of creation is added to a property car:

![Date of creation](images/creation_date.png)


## Installation
Double klick on `org-mode-capture.alfredworkflow` to add it to Alfred's set of workflows. Then you need to set the path to your existing org-mode inbox file in both python script nodes (absolute notation of the path is necessary). You can also change the delimiter pattern to distinguish between head and body elements and disable the relative date replacement by setting it to `False`:

```python
org.inbox_file = '/Users/Alex/Documents/Planung/Planning/Inbox.org'
org.delimiter = ':: '
org.add_creation_date = True
org.replace_relative_dates = True
```

![Edit the python script nodes within Alfred](images/workflow.png)

## Supported modes of notification

If you don't use growl, you can change the notification nodes in the alfred workflows to apple's notification centre:

![Notification system](images/supported_notificaitons.png)
