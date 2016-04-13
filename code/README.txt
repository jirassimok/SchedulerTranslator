WPI Scheduler database translator

Retrieves and translates the new Scheduler's database from
wpi.collegescheduler.com and writes it to a local database, which can be
translated into the old scheduler's schedb xml format.


To get a database from the server, run as:
python3 Main.py get DATABASE_PATH

To transcribe the database to an xml, run as:
python3 Main.py parse PORT DATABASE_PATH IO_PATH

If not specified, PORT, DATABASE_PATH, and IO_PATH default to 8000,
"../DATABASE", and "../io", respectively.

Run requirements:
    Both commands must be run from the code directory.
    Port PORT must be free for to parse the database.
    DATABASE_PATH must exist as a directory relative to the code directory both
      to get the database and to parse the data.
    To parse the data, IO_PATH must exist as a directory relative to
      DATABASE_PATH.

    To get the database, the term directories may need to exist beforehand.

Also, on certain operating systems (OS X 10.10), parsing will prompt a dialog
regarding accepting incoming connections. If this prompt is not dismissed
within 5 seconds, the program may fail to run.
