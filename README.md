# simple-request-cache

Command line arguments accepted can be seen with `python main.py --help`:

```
python main.py --help
usage: main.py [-h] [--port PORT] [--maxelapsed MAXELAPSED] [--baseurl BASEURL] [--nodebug]

Start simple request cache service.

options:
  -h, --help            show this help message and exit
  --port PORT           port to use
  --maxelapsed MAXELAPSED
                        max time (integer seconds) before invalidating cache
  --baseurl BASEURL     base url prefix for all requests
  --nodebug             disables hot reloading and debug messages
```