#!/usr/bin/env python3
import sys
import time
import threading
import requests

def fetch(url):
    try:
        r = requests.get(url)
        print(f"Fetched {url} -> {len(r.content)} bytes")
    except Exception as e:
        print(f"Error fetching {url}: {e}")

def run_test(url_file, concurrency):
    with open(url_file) as f:
        urls = [line.strip() for line in f if line.strip()]

    start = time.time()

    if concurrency == 1:
        # Sequential
        for u in urls:
            fetch(u)
    else:
        # Concurrent
        threads = []
        for u in urls:
            t = threading.Thread(target=fetch, args=(u,))
            t.start()
            threads.append(t)

            # limit active threads
            while len([t for t in threads if t.is_alive()]) >= concurrency:
                time.sleep(0.1)

        for t in threads:
            t.join()

    end = time.time()
    elapsed = end - start
    print(f"\nCompleted {len(urls)} URLs with concurrency={concurrency} in {elapsed:.2f}s\n")
    return elapsed

def main():
    if len(sys.argv) != 2:
        print("Usage: ./test_script.py <url_list.txt>")
        sys.exit(1)

    url_file = sys.argv[1]

    print("Running sequential test...")
    t1 = run_test(url_file, concurrency=1)

    print("Running concurrent test (10 connections)...")
    t2 = run_test(url_file, concurrency=10)

    print(f"Speedup = {t1 / t2:.2f}x faster")

if __name__ == "__main__":
    main()
