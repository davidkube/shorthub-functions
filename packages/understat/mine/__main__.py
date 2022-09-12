import asyncio
import aiohttp
from datetime import datetime
import pymongo
from pymongo.write_concern import WriteConcern
import sys

from understat import Understat


LEAGUES = {
      "epl": "EPL",
      "la_liga": "La_liga",
      "bundesliga": "Bundesliga",
      "serie_a": "Serie_A",
      "ligue_1": "Ligue_1",
      "rfpl": "RFPL"
}

START_SEASON = 2014

def rename_id(dict):
      dict['_id'] = dict.pop('id')
      return dict

async def main_two(args):
      async with aiohttp.ClientSession() as session:
            understat = Understat(session)
            list_of_matches = await understat.get_league_matches(args[1],args[2]) 

            reindexed = [rename_id(match) for match  in list_of_matches]
            args[0].delete_many( { '_id' : { '$in': [match['_id'] for match in reindexed] } } );
            return args[0].insert_many(reindexed).inserted_ids
            
      
def main(args):
      LEAGUE = args['league']
      SEASON = args['season']

      response = ""

      cont = True
      if LEAGUE not in LEAGUES.values():
            response += 'Invalid League'
            cont = False
      currentYear = datetime.now().year
      if int(SEASON) not in range(START_SEASON,currentYear+1):
            response +='Invalid Season : ' + str(SEASON) + ' not in (' + ', '.join([str(x) for x in range(START_SEASON,currentYear+1)]) + ')'
            cont = False
      if cont:
            CLIENT = pymongo.MongoClient("mongodb+srv://doadmin:u807mD45kl192cNP@shorthub-9b85bbdd.mongo.ondigitalocean.com/understat?tls=true&authSource=admin&replicaSet=shorthub")
            DB = CLIENT["understat"]
            COLL = DB["matches"]
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = '(' + ', '.join([str(x) for x in loop.run_until_complete(main_two([COLL,LEAGUE,SEASON]))]) + ')'
            return {"statusCode": 200, "body": response}
      return {"statusCode": 400, "body" : response}