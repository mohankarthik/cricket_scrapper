import logging
import multiprocessing
from typing import List
import requests
import json

BCCI_BASE_URL = "https://scores.bcci.tv"
BCCI_DOMESTIC_COMPEITION_URL = f"{BCCI_BASE_URL}/feeds/competition.js"
BCCI_INTERNATIONAL_COMPETITION_URL = f"{BCCI_BASE_URL}/matchcentre/mc/competition.js"


class BcciScrape:
    @staticmethod
    def _cleanCompetitionResponse(response: str) -> List[dict]:
        return json.loads(response[13:-2])["competition"]

    @staticmethod
    def _cleanScheduleResponse(response: str) -> List[dict]:
        return json.loads(response[14:-2])["Matchsummary"]

    @staticmethod
    def _cleanSummaryResponse(response: str) -> dict:
        return json.loads(response[22:-2])["MatchSummary"][0]

    @staticmethod
    def _cleanSquad(response: str) -> List[dict]:
        return json.loads(response[8:-2])

    @staticmethod
    def _cleanInnings(response: str) -> List[dict]:
        return json.loads(response[10:-2])

    def getCompetitions(this):
        logging.info(f"Getting list of all competitions")
        domestic = BcciScrape._cleanCompetitionResponse(
            requests.get(BCCI_DOMESTIC_COMPEITION_URL).text
        )
        international = BcciScrape._cleanCompetitionResponse(
            requests.get(BCCI_INTERNATIONAL_COMPETITION_URL).text
        )
        for competition in domestic:
            competition["type"] = "domestic"
        for competition in international:
            competition["type"] = "international"
            
        logging.debug(f"Got a total of {len(domestic)} domenstic competitions and {len(international)} international competitions")
        return domestic + international

    def getMatchSummaryForCompetition(
        this, competition: dict, ignore_list: List[str] = []
    ) -> List[dict]:
        logging.info(f"Getting match details for competition: {competition['CompetitionName']}")
        competitionId = competition["CompetitionID"]
        competitionType = competition["type"]

        if competitionType == "domestic":
            BCCI_SCHEDULE_URL = (
                f"{BCCI_BASE_URL}/feeds/{competitionId}-matchschedule.js"
            )
        else:
            BCCI_SCHEDULE_URL = f"{BCCI_BASE_URL}/feeds-international/scoringfeeds/{competitionId}-matchschedule.js"

        try:
            matches = BcciScrape._cleanScheduleResponse(
                requests.get(BCCI_SCHEDULE_URL).text
            )
            logging.debug(f"Got a total of {len(matches)} matches for {competition['CompetitionName']}")
            matches = [
                match
                for match in matches
                if (
                    match["MatchStatus"] == "Post"
                    and match["MatchID"] not in ignore_list
                )
            ]
            logging.debug(f"After filtering ignore list and not compelted, we've {len(matches)} matches for {competition['CompetitionName']}")

            for match in matches:
                match["type"] = competitionType
                match = BcciScrape.augmentMatchDetails(match)

            return matches

        except:
            return []

    @staticmethod
    def augmentMatchDetails(match: dict) -> dict:
        logging.info(f"Updating match details for {match['MatchName']}")
        matchId = match["MatchID"]
        matchType = match["type"]

        if matchType == "domestic":
            BCCI_SUMMARY_URL = f"{BCCI_BASE_URL}/feeds/{matchId}-matchsummary.js"
            BCCI_SQUAD_URL = f"{BCCI_BASE_URL}/feeds/{matchId}-squad.js"
            BCCI_INNINGS_URL = f"{BCCI_BASE_URL}/feeds/{matchId}-Innings"
        else:
            BCCI_SUMMARY_URL = f"{BCCI_BASE_URL}/feeds-international/scoringfeeds/{matchId}-matchsummary.js"
            BCCI_SQUAD_URL = (
                f"{BCCI_BASE_URL}/feeds-international/scoringfeeds/{matchId}-squad.js"
            )
            BCCI_INNINGS_URL = (
                f"{BCCI_BASE_URL}/feeds-international/scoringfeeds/{matchId}"
            )

        matchSummary = BcciScrape._cleanSummaryResponse(
            requests.get(BCCI_SUMMARY_URL).text
        )
        match.update(matchSummary)

        squadDetails = BcciScrape._cleanSquad(requests.get(BCCI_SQUAD_URL).text)
        match["squad"] = squadDetails

        # If the match wasn't abandoned, then get the innings details
        if match["CurrentInnings"] != "":
            currentInnings = int(match["CurrentInnings"])
            for innings in range(1, currentInnings + 1):
                inningsDetails = BcciScrape._cleanInnings(
                    requests.get(f"{BCCI_INNINGS_URL}{innings}.js").text
                )
                match.update(inningsDetails)

        return match


def test() -> None:
    scrapper = BcciScrape()
    competitions = scrapper.getCompetitions()
    matches = []
    for competition in competitions[0:1]:
        print(f"Getting matches for {competition['CompetitionID']}")
        matches += scrapper.getMatchSummaryForCompetition(competition=competition)

    f = open("dump.json", "a")
    f.write(json.dumps(matches))
    f.close()


if __name__ == "__main__":
    test()
