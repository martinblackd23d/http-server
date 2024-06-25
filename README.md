# Files:
HelloWorld.html:
- Default page

README.md:
- This README

threadedwebserver.py
- An HTTP server that can handle multiple requests simultaneously by spawning a new thread for each request.

webclient.py
- A client that makes an HTTP request to a specified host, port and file, and processes and prints the response

webserver.py
- An HTTP server that handles a single collection at a time and responds with either the requested file or an appropriate error message.

# Run
Normal operation:
```python3 webserver.py```
or
```python3 threadedserver.py```

then
```python3 webclient.py localhost 56006 HelloWorld.html```
or open
[http://localhost:56006/HelloWorld.html]()

Testing multithreading:
```python3 threadedserver.py --slow```
This inserts a 5 second delay to test multiple connections