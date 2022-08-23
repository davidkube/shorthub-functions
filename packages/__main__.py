import asyncio
import json
import aiohttp

from understat.understat import Understat

async def main(args):
      async with aiohttp.ClientSession() as session:
            understat = Understat(session)
            test = await understat.get_league_matches('EPL',2021)
            print(json.dumps(test))
            
      
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main([]))

    