# CN
# Simple HTTP Server

## How to Run
Windows:
    python http_server.py -p 20001

Mac/Linux:
    ./http_server.py -p 20001
    (Make sure file is executable: chmod +x http_server.py)

Then open your browser and go to:
    http://localhost:20001/

## Limitations
- Only supports GET
- HTTP/1.0
- One request at a time
- No HTTPS or POST support

## Questions
1. Difference from Apache:
   Apache supports multi-threading, modules, dynamic content, HTTPS, etc.
   Our server is single-threaded, static, basic HTTP/1.0.

2. Restrict to Chrome:
   Check the "User-Agent" header in the request.
   If it doesn’t contain "Chrome", respond with 403 Forbidden.
