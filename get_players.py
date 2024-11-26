"""
This module fetches Dota 2 player leaderboard data from the STRATZ API.
"""

from typing import Dict, List
import collections
import json
import os
from pathlib import Path

import pandas as pd
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Constants
DIVISIONS = ["AMERICAS", "SE_ASIA", "EUROPE", "CHINA"]
API_URL = "https://api.stratz.com/graphql"

# GraphQL query for fetching leaderboard data
query = gql(
    """
    query GetPlayersLeaderboards($leaderboardRequestVariable: FilterSeasonLeaderboardRequestType, $skipUserFollowingData: Boolean!, $skip: Long, $take: Long) {
        leaderboard {
            season(request: $leaderboardRequestVariable) {
                playerCount
                players(skip: $skip, take: $take) {
                    steamAccountId
                    steamAccount {
                        ...LeaderboardSteamAccount
                        __typename
                    }
                    rank
                    rankShift
                    position
                    __typename
                }
                countryData {
                    countryCode
                    playerCount
                    __typename
                }
                positionData {
                    position
                    playerCount
                    __typename
                }
                teamData {
                    id
                    name
                    __typename
                }
                __typename
            }
            __typename
        }
        stratz @skip(if: $skipUserFollowingData) {
            user {
                following {
                    steamAccount {
                        ...FollowingSteamAccount
                        __typename
                    }
                    __typename
                }
                __typename
            }
            __typename
        }
    }

    fragment LeaderboardSteamAccount on SteamAccountType {
        id
        countryCode
        isAnonymous
        proSteamAccount {
            countries
            __typename
        }
        ...TeamTagPlayerNameColSteamAccountTypeFragment
        __typename
    }

    fragment TeamTagPlayerNameColSteamAccountTypeFragment on SteamAccountType {
        id
        name
        proSteamAccount {
            name
            team {
                tag
                id
                name
                __typename
            }
            __typename
        }
        __typename
    }

    fragment FollowingSteamAccount on SteamAccountType {
        rankShift
        seasonLeaderboardRank
        seasonLeaderboardDivisionId
        proSteamAccount {
            position
            __typename
        }
        ...LeaderboardSteamAccount
        __typename
    }
    """
)

def get_api_key() -> str:
    """Get the API key from environment variable."""
    api_key = os.environ.get("STRATZ_API_KEY")
    if not api_key:
        raise ValueError("STRATZ_API_KEY environment variable is not set")
    return api_key

def setup_client() -> Client:
    """Set up and return a GraphQL client with proper authentication."""
    transport = RequestsHTTPTransport(
        url=API_URL,
        headers={"Authorization": f"Bearer {get_api_key()}", "Content-Type": "application/json"},
        use_json=True,
    )
    return Client(transport=transport, fetch_schema_from_transport=True)

def get_data_files() -> None:
    """Fetch player data for each division and save to JSON files."""
    client = setup_client()
    players_dir = Path("players")
    players_dir.mkdir(exist_ok=True)

    for division in DIVISIONS:
        try:
            response = client.execute(
                query,
                variable_values={
                    "leaderboardRequestVariable": {"leaderBoardDivision": division},
                    "skip": 0,
                    "take": 10000,
                    "skipUserFollowingData": True,
                },
            )
            
            output_file = players_dir / f"{division}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(response, f, ensure_ascii=False, indent=4)
                
        except Exception as e:
            print(f"Error fetching data for {division}: {str(e)}")

def merge_data_files() -> None:
    """Merge all division JSON files into a single CSV file."""
    data: Dict[str, List] = collections.defaultdict(list)

    for division in DIVISIONS:
        try:
            with open(f"players/{division}.json", "r", encoding="utf-8") as f:
                raw_data = json.load(f)

                for player in raw_data["leaderboard"]["season"]["players"]:
                    data["steamAccountId"].append(player["steamAccount"]["id"])
                    data["countryCode"].append(player["steamAccount"]["countryCode"])
                    data["isAnonymous"].append(player["steamAccount"]["isAnonymous"])
                    data["name"].append(player["steamAccount"]["name"])
                    data["rank"].append(player["rank"])
                    data["position"].append(player["position"])
                    data["division"].append(division)

        except Exception as e:
            print(f"Error processing {division} data: {str(e)}")

    pd.DataFrame(data).to_csv("players.csv", index=False)

def main() -> None:
    """Main function to orchestrate the data collection and processing pipeline."""
    get_data_files()
    merge_data_files()

if __name__ == "__main__":
    main()
