WPI Scheduler database translator

Retrieves and translates the new Scheduler's database from
wpi.collegescheduler.com and writes it to a local database, which can be
translated into the old scheduler's schedb xml format.

Current version: 2.0
TODO: Improve ease of use - stop using testmain.py as the main file.

To get a database from the server, run with:
Main.py get DATABASE_PATH

To transcribe the database to an xml:
1. Make the code directory the working directory.

2. Enter a python interpreter.

3. Run this code:
>>> import hostdb
>>> hostdb.PORT = 8001
>>> hostdb.DATABASE_PATH = "../DATABASE"  # set to the path to your database dir
>>> hostdb.run_database_server()

3. Run testing/testmain.py as follows, with FILEPATH being the path to testmain
   relative to the database directory.
   a. IPython: %run FILEPATH
   b. Standard interpreter: exec(open("FILEPATH").read(), globals())

4. Run this code: (change the filename as appropriate)
>>> hostdb.close_database_server()
>>> with open("new_v1.1.schedb", "w+") as schedbfile:
...     schedbfile.write(str(schedb))


######## ######## ######## ######## ######## ######## ######## ########

Changes to old Scheduler required to make new data work fully:
Add a flag that makes sections un-addable, or add "subsections" or "subclasses".
Subclasses might be easiest/best: Within a course, have separate areas for
lectures and labs etc, and allow one from each area to be selected.

######## ######## ######## ######## ######## ######## ######## ########


Former instructions: Besides the transcription instructions, these may still
hold. The transcription isntructions are likely to fail due to code changes.

To transcribe the database to an xml, run with:
Main.py parse PORT DATABASE_PATH IO_PATH

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
