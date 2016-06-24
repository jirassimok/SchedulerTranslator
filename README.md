# WPI Scheduler database translator #

Retrieves and translates the new Scheduler's database from wpi.collegescheduler.com and writes it to a local database, which can be translated into the old scheduler's schedb xml format.

Current version: 2.0

## Usage ##
Usage information can be found with `-h` or `--help`. With no arguments, it will ask for username and password, then fetch and parse the database. Arguments are shown below:

| Argument          | Function                                                           |
|-------------------|--------------------------------------------------------------------|
| `--database`      | Path for the database                                              |
| `--pwfile`        | A password file (username on the first line, password on the next) |
| `-o`, `--output`  | Path for the output file                                           |
| `--prompt`        | Prompt often                                                       |
| `-v`, `--verbose` | Print extra information                                            |
| `-l`, `--local`   | Use the local database generated with `-g`                         |
| `-g`, `--get`     | Generate a local database for use with `-l`                        |
| `--no-parse`      | Don't parse the data. Implies `-g`                                 |
|                   |                                                                    |

## TODO ##

  * [ ] Run from parent directory, so this can be a child of the real scheduler.


Changes to old Scheduler required to make new data work fully:

  * Add a flag that makes sections un-addable, or add "subsections" or "subclasses".
  * Subclasses might be easiest/best: Within a course, have separate areas for lectures and labs etc, and allow one from each area to be selected.

