import yaml
import requests
from urllib.parse import quote
import tiktoken
import time
import asyncio
import os
import aiohttp


def memorize(content: str, speaker: str, timestamp: float):
    # Get the current working directory and create the file path
    cwd = os.getcwd()
    filename = os.path.join(cwd, 'temp_memo.yaml')

    # Initialize an empty list for data
    data = []

    if os.path.isfile(filename):
        # Load the data from the YAML file if it exists
        with open(filename, 'r') as file:
            loaded_data = yaml.safe_load(file)
            if loaded_data is not None:
                data = loaded_data

    # Create a new entry
    new_entry = {
        'content': content,
        'speaker': speaker,
        'timestamp': timestamp
    }

    # Append the new entry to the list
    data.append(new_entry)

    # Write the updated data back to the YAML file
    with open(filename, 'w') as file:
        yaml.dump_all([data], file, explicit_start=True)


def store_in_REMO(entry: dict):
    formatted_memory = quote(entry['content'])
    speaker = entry['speaker']
    timestamp = float(entry['timestamp'])
    response = requests.post(f"http://localhost:8000/add_message?message={formatted_memory}&speaker=User&timestamp={timestamp}")
    return response.status_code == 200


def pop_oldest():
    # Load the data from the YAML file
    with open('temp_memo.yaml', 'r') as file:
        data = yaml.safe_load(file)

    oldest_entry = data.pop(0)
    
    if store_in_REMO(oldest_entry):
        print(f"Stored entry in long-term memory: {oldest_entry}")

        # Update the YAML file after removing the oldest entry
        with open('temp_memo.yaml', 'w') as file:
            yaml.dump(data, file)
    else:
        print("Failed to store entry in long-term memory. Retrying...")


def form_corpus():
    # Get the current working directory and create the file path
    cwd = os.getcwd()
    filename = os.path.join(cwd, 'temp_memo.yaml')

    data = []

    if os.path.isfile(filename):
        # Load the data from the YAML file if it exists
        with open(filename, 'r') as file:
            loaded_data = yaml.safe_load(file)
            if loaded_data is not None:
                data = loaded_data

    corpus = ''

    for entry in data:
        corpus += f'{entry["content"]}\n'

    return corpus


async def rebuild_tree():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8000/rebuild_tree') as response:
            print("REBUILT REMO TREE")


def handle_corpus(pop=False, tokens=3000):
    corpus = form_corpus()
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0301")
    corpus_tokens = len(encoding.encode(corpus)) + 4

    if corpus_tokens > tokens:
        pop_oldest()
        return handle_corpus(pop=True, tokens=tokens)  # Call the function recursively
    else:
        if pop is True:
            # Create a new event loop and run the coroutine inside it
            loop = asyncio.get_event_loop()
            task = loop.create_task(rebuild_tree())  # Schedule the coroutine
        return corpus  # Base case: return the corpus when the condition is not met
