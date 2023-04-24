#  Temporally Egressive Memory Partitioning Organizer (TEMPO)
Human brains have 2 kinds of memory: short-term (TEMPO) and long-term ([REMO](https://github.com/daveshap/REMO_Framework)).

### Purpose
REMO is great at handling old information, but is inefficient when dealing with quick recall of fresh information. It is also left to the user to manage various calls to its API. TEMPO takes care of both of these issues. TEMPO's API only has `memorize` and `remember`; everything else, including REMO memories, are handled automatically.

![image](https://user-images.githubusercontent.com/123516285/233898760-8b797873-dcd7-46ff-a81b-74406f8d76d0.png)

## Setup
1. Launch REMO (TEMPO expects this to be on port 8000)
2. Launch TEMPO (port 8001 if you're using the provided LangFlow json)
3. Launch LangFlow and import TEMPO-LangFlow.json
4. Plug in you OpenAI API key into the biggest node on the left
5. Chat...

```
uvicorn tempo:app --reload --port 8001
```

## How it works
#### TEMPO
- A list of dictionaries (each containing a singular memory) is stored in a yaml file. 
- All of these memories come in through POST requests to TEMPO's `memorize` endpoint.
- Similarly, GET requests to the `remember` endpoint fetch the entirety of working memory.
- When the working memory exceeds 1000 tokens (this can be easily changed), oldest memories are popped to long-term memory in REMO until the working memory is under 1000 tokens again.
- Rebuilding of REMO's memory tree is asynchronously automated by TEMPO, so new memories entering REMO are immediately accessible without halting the agent's response (faster).
#### Flow
- The included flow json allows you to quickly test this out in LangFlow before you integrate it into your own architecture.
- Various Python methods that communicate with the TEMPO and REMO APIs are given to the agent as tools.
- The rest of the work went into the prompt prefix that explains when it's appropriate for the agent to use particular tools.
