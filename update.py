from bcci_scrape import BcciScrape
from cric_data_store import CricDataStore
import logging
from dotenv import load_dotenv

def main() -> None:
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Load the env files
    load_dotenv()
    
    scrapper = BcciScrape()
    dataStore = CricDataStore()
    dataStore.clear()
    
    competitions = scrapper.getCompetitions()
    for competition in competitions:
        ignore_list = dataStore.getMatchesForCompetition(competitionId=competition["CompetitionID"])
        matches = scrapper.getMatchSummaryForCompetition(competition=competition, ignore_list=ignore_list)
        
        for match in matches:
            dataStore.insertMatch(match=match)

if __name__ == "__main__":
    main()