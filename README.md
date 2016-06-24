# WPI Scheduler database translator #

Retrieves and translates the new Scheduler's database from wpi.collegescheduler.com and writes it to a local database, which can be translated into the old scheduler's schedb xml format.

Current version: 2.0

## Usage ##
Main.py has two modes: `get` and `parse`. `get` will build a local copy of the collegescheduler database, while `parse` will use that database to create the schedb xml file.

### Arguments ###
Only the mode (get/parse) is required, but there are several other arguments. Some arguments are only used in one mode. The table below shows which arguments function in which modes.

| Argument          | Function                    | Mode  |
|-------------------|-----------------------------|-------|
| `--database`      | Path for the database       | both  |
| `--pwfile`        | A password file             | get   |
| `-o`, `--output`  | Path for the output file    | parse |
| `-p`, `--port`    | Port for the local database | parse |
| `--prompt`        | Prompt often                | both  |
| `-v`, `--verbose` | Print extra information     | both  |

`--pwfile` takes a file with the username on one line, and the password on the next

## TODO ##

  * [ ] Run from parent directory, so this can be a child of the real scheduler.


Changes to old Scheduler required to make new data work fully:

  * Add a flag that makes sections un-addable, or add "subsections" or "subclasses".
  * Subclasses might be easiest/best: Within a course, have separate areas for lectures and labs etc, and allow one from each area to be selected.

