from scraper.vsync import ImmoCrawler
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
    crawler.to_csv("speed")


if __name__ == "__main__":
    asyncio.run(main())
    




# Time spent inside the loop: 16.537395875013317 seconds.
# Time spent inside the loop: 13.28181429200049 seconds.
# Time spent inside the loop: 917.5551847500028 seconds. -> 50 pages (old)
# Time spent inside the loop: 91.03166958299698 seconds. -> 50 pages (Async)
# Time spent inside the loop: 611.8511871249939 seconds. -> 333 pages (Async, semaphore = 10)
    
# Time spent inside the loop: 39.523070584007655 seconds. -> 20 pages (Async, semaphore = 15)
# Time spent inside the loop: 26.737354500000947 seconds. -> 20 pages (Async, semaphore = 20)
# Time spent inside the loop: 28.12415995799529 seconds. -> 20 pages (Async, semaphore = 25)
# Time spent inside the loop: 31.825474792000023 seconds. -> 20 pages (Async, semaphore = 30)
    
    # Conclusion: Using 20 as parameter for semaphore is the quickest and probably the max. 

    # Test of numbers near 20, maybe find slightly faster? 

# Time spent inside the loop: 27.49819800000114 seconds. -> 20pages (Async, semaphore = 21)
# Time spent inside the loop: 35.979889332986204 seconds. -> 20pages (Async, semaphore = 19)
# Time spent inside the loop: 40.390866250003455 seconds. -> 20pages (Async, semaphore = 20)
    
    # guess: I think it has like a limit per minut or something? 
    # confirm guess?: waited a minut and tried again. Got: Time spent inside the loop: 27.688576749991626 seconds
    # -> 20pages (Async, semaphore = 20).

    # let's try a crazy number! 

# Time spent inside the loop: 27.659887083995272 seconds. -> 20 pages (Async, semaphore = 100)
# Time spent inside the loop: 28.53670566699293 seconds. -> 20 pages (Async, semaphore = 1000)
# Time spent inside the loop: 27.190235500005656 seconds. -> 20 pages (Async, semaphore = 5000)

#Time spent inside the loop: 27.420335792005062 seconds. -> 20 pages (Async, semaphore = 10000)