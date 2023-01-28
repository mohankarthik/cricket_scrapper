import json
import os
from typing import List
import pymongo


class CricDataStore:
    def __init__(self) -> None:
        self.myclient = pymongo.MongoClient(os.environ.get("MONGO_URI"))
        self.mydb = self.myclient[os.environ.get("MONGO_DB")]
        self.colBcci = self.mydb[os.environ.get("MONGO_COL")]
        
    def clear(self) -> None:
        self.colBcci.drop()

    def insertMatch(self, match: dict) -> None:
        self.colBcci.insert_one(match)

    def getMatchesForCompetition(self, competitionId: str) -> List[str]:
        result = self.colBcci.find(
            {"CompetitionID": competitionId}, {"_id": 0, "MatchID": 1}
        )
        matches = []
        for row in result:
            matches.append(row["MatchID"])
        return matches


def test() -> None:
    from dotenv import load_dotenv
    load_dotenv()
    dataStore = CricDataStore()
    f = open("test.json", "r")
    data = json.loads(f.read())
    dataStore.insertMatch(data)
    print(dataStore.getMatchesForCompetition("251"))


if __name__ == "__main__":
    test()
