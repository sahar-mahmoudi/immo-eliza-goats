from scraper.immoscraper import ImmoCrawler
import asyncio
import sys
import time
import threading

# Function to display a spinner in a separate thread
def spinner():
    while True:
        for cursor in '|/-\\':
            sys.stdout.write(cursor)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')

async def main():
    print("\nImmoCrawler is running...", end="", flush=True)
    
    # Start spinner in a separate thread
    threading.Thread(target=spinner, daemon=True).start()  
    
    list=["west-flanders"]
    for city in list:
        # Create an instance of ImmoCrawler
        crawler = ImmoCrawler(city="west-flanders")
    
    # Asynchronously fetch and extract property data
    await crawler.get_properties()
    
    # Convert the collected property data to a CSV file
    crawler.to_csv("data")


if __name__ == "__main__":
    # Run the main function using asyncio
    asyncio.run(main())

