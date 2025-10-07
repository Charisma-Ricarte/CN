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
1. What is the difference between http_server  (what  you wrote) and Apache?
   
   Apache supports multi-threading, modules, dynamic content, HTTPS, etc. Our server is single-threaded, static, basic HTTP/1.0. It is simplified and designed to demonstrate how the HTTP protocal would occur and work while Apache is developed fully. It is a prodection grade web server that is already used for real world applications. It is night and day with the differences between our http_server and Apache.

2. Some web sites allow only certain browsers(e.g., Chrome) to download content from them. How can you write http_server to support this feature?   Be specific about where/what code is needed.

   Restricting it to chrome browsers so that only their browsers will be able to acess it. Check the "User-Agent" header in the request. The header would identify the opperating and browser system that the client is using. We would then have a handle_client() function that would, after receiving and decoding, the server would search for the word chrome. If it doesn’t contain "Chrome", respond with 403 Forbidden. The response would be indicated to show that access would be denied because some of the criteria from the browser was not met. This check would enforce browser access controls that would act like some real world websites that would limit compatability.

