from test_final import ImmoCrawler
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
    
    # Create an instance of ImmoCrawler
    crawler = ImmoCrawler()
    
    # Asynchronously fetch and extract property data
    await crawler.get_properties(1)
    
    # Convert the collected property data to a CSV file
    crawler.to_csv("data")


if __name__ == "__main__":
    # Run the main function using asyncio
    asyncio.run(main())

    # Took 374.3080553329928 -> 2province 10 somo 
    # Took 1636.436235000001 -> All province 10 somow -> 1377 houses
    # Took 320.27851666700735 -> all province 10 somo -> !Not in order though! -> need to put an await somewhere! 
    # Took 185.44270083399897 -> all provinces 15 somo -> ""  "" "" ""             " "        ""        ""