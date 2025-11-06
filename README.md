1. Overview
---------------------------------------------------------------
This assignment extends the sequential HTTP server from HW3
to support multiple concurrent client connections. The server
uses threads to handle simultaneous requests, while enforcing
connection limits per client and overall system-wide.

Program name:
    http_server_conc.py

It serves static files from the current directory and subfolders,
responding to simple HTTP/1.0 GET requests.


2. How to Run
---------------------------------------------------------------
Usage:
    ./http_server_conc.py -p <port> -maxclient <numconn> -maxtotal <numconn>

Example:
    ./http_server_conc.py -p 20001 -maxclient 12 -maxtotal 60
Make sure to have requests installed:
  pip install requests

In this example:
 - The server listens on port 20001
 - Each client IP can open at most 12 concurrent connections
 - The server allows up to 60 concurrent connections total


3. How to Test
---------------------------------------------------------------
1. Place test files (HTML, images, PDFs, etc.) in the same
   directory as the server or inside subdirectories.

2. Launch the server with your desired limits.

3. Use your HTTP client from HW2 to download URLs listed in:
       https://zechuncao.com/teaching/csci4406/testfiles/testscript1.txt
       https://zechuncao.com/teaching/csci4406/testfiles/testscript2.txt

   Test both sequentially (1 connection) and concurrently (10 connections).

4. Measure and record download times, then compute speedup:
       speedup = sequential_time / concurrent_time

________________________________________________________________________________________________________________________________________________________________________________
Required Questions
________________________________________________________________________________________________________________________________________________________________________________
(1.)What is your strategy for identifying unique clients?
    Using the IP address and source port helps distinguish unique clients. 
    This ensures that even if they share the same IP from a router, each connection is counted per client.

(2.)How do you prevent the clients from opening more connections once they have opened the maximum number of connections?
    There is a counter to signify the maximum number of connections a client can have.
    If the limit is reached, they are no longer able to open any more connections.

(3.)Report the times and speedup for concurrent fetch of the URLs in testcase 1 and 2 with the stock http server.

    Test 1: 
    Sequential = 218.35 s
    Concurrent = 27.08 s
    Speedup = 8.48x faster
   
    Test 2: 
    Sequential = 24.37 s
    Concurrent = 9.45 s
    Speedup = 2.45x faster

(4.)Report the times and speedup for concurrent fetch of the URLs in testcase 1 and 2 with your http_server_conc. Are these numbers same as above? Why or why not?

    Test 1: 
    Sequential = 223.73 s  
    Concurrent = 21.00 s  
    Speedup = 9.49× faster

    
    Test 2: 
    Sequential = 19.31 s  
    Concurrent = 8.23 s  
    Speedup = 2.35× faster

No, they’re not the same. The concurrent HTTP server performs better because it uses multiple threads to handle requests in parallel, reducing wait time and improving performance, especially under heavier loads. This is most noticeable in Test 1, where more URLs are fetched, while in smaller tests like Test 2, the speedup is smaller due to fewer concurrent requests.
________________________________________________________________________________________________________________________________________________________________________________
