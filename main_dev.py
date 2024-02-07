from test_final import ImmoCrawler

import asyncio
import sys
import time
import threading
def spinner():
    while True:
        for cursor in '|/-\\':
            sys.stdout.write(cursor)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')

async def main():
    print("\nImmoCrawler is running...", end="", flush=True)
    threading.Thread(target=spinner, daemon=True).start()  # Start spinner in a separate thread
    crawler = ImmoCrawler()
    await crawler.get_properties()
    crawler.to_csv("SPEEEEDY_MY")


if __name__ == "__main__":

    asyncio.run(main())