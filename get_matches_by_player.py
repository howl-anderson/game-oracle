"""
This module fetches match data for Dota 2 players using the STRATZ API.
"""

from typing import List, Dict, Any
import json
import os
from pathlib import Path

import pandas as pd
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.exceptions import TransportQueryError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_not_exception_type

# Constants
BATCH_SIZE = 5
PLAYERS_FILE = "players.csv"
OUTPUT_DIR = "players_matches"
GAME_VERSION = 176
API_URL = "https://api.stratz.com/graphql"

# GraphQL query for fetching match data
MATCH_QUERY = gql("""
    query GetMatches($steam_account_ids: [Long]!) {
        players(steamAccountIds: $steam_account_ids) {
            steamAccountId,
            matchCount,
            winCount,
            matches(request: {skip: 0, take: 100, gameVersionIds: [176]}) {
                id
                pickBans {
                    order
                    isPick
                    isRadiant
                    heroId
                }
                didRadiantWin
            }
        }
    }
""")

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

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_not_exception_type(TransportQueryError),
    reraise=True,
)
def retry_client_execute(client: Client, query: gql, variable_values: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a GraphQL query with retry logic."""
    return client.execute(query, variable_values=variable_values)

def get_player_ids() -> List[int]:
    """Read player IDs from the CSV file."""
    pd_data = pd.read_csv(PLAYERS_FILE)
    return pd_data["steamAccountId"].tolist()

def fetch_matches() -> None:
    """Fetch match data for players in batches and save to JSON files."""
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    
    client = setup_client()
    id_list = get_player_ids()
    
    for i, start in enumerate(range(0, len(id_list) + BATCH_SIZE, BATCH_SIZE)):
        store_file = output_path / f"{i}.json"
        
        if store_file.exists():
            continue
            
        id_list_slice = id_list[start : start + BATCH_SIZE]
        if not id_list_slice:
            continue
            
        try:
            response = retry_client_execute(
                client,
                MATCH_QUERY,
                variable_values={"steam_account_ids": id_list_slice}
            )
            
            with open(store_file, "w", encoding="utf-8") as f:
                json.dump(response, f, ensure_ascii=False, indent=4)
                
            print(f"Successfully processed batch {i}")
            
        except Exception as e:
            print(f"Error processing batch {i}: {str(e)}")

def main() -> None:
    """Main function to orchestrate the match data collection process."""
    try:
        fetch_matches()
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()