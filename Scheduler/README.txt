
2016-04-05,12

Jacob I. Komissar

TODO: Replace this with a newer version of the scheduler.

This is a duplicate of WPI's previous scheduler-organizing tool.

Most of the files were downloaded from scheduler.wpi.edu/..., except the main
html file, which no longer is available online, having been replaced by the new,
much-inferior course planner.

The file WPIScheduler.html is the main page. It can be opened directly in
Firefox, but will not work in Safari or Google Chrome, because of issues caused
by the file "56F3A1425FF11F97127E67E9FA3ED271.cache.js".

The courses shown on the page are read from new_v1.1.schedb.


To run the server, run the following command in this directory:

python3 -m http.server PORT

Where PORT is the port to serve the scheduler at.
The scheduler can then be accessed at localhost:8000/WPIScheduler.html


######## Author's personal notes; may not apply ########

To view the page in all browsers, run the SERVER.command file. This uses makes
  the page available at localhost:8000/WPIScheduler.html with Python's
  SimpleHTTPServer module.
Deny the process the ability to accept incoming connections.
To close the server, kill the process running the server (ctrl+C, ctrl+D, or
  closing the window should all work).

Alternatively, use the Brackets application's live preview function to create
a similar server.



