"""
This module converts raw Dota 2 match and hero data into a standardized public dataset format.
It processes two main data files:
1. matches.jsonl - Contains match data with original match IDs
2. heroes.json - Contains hero information from the game
"""

from typing import List, Dict, Any
import json
from pathlib import Path
import jsonlines

# Constants
MATCHES_FILE = "matches.jsonl"
HEROES_FILE = "heroes.json"

def process_matches(input_data: Any) -> Dict[str, Any]:
    """Process match data and standardize format.
    
    Args:
        input_data: Either a file path (str) or a dictionary containing match data
        
    Returns:
        Dict containing processed match data
    """
    if isinstance(input_data, str):
        input_path = Path(input_data)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_data}")
            
        with jsonlines.open(input_data) as reader:
            dataset = []
            for id, obj in enumerate(reader):
                obj["match_id"] = id  # Reassign match_id to be sequential
                dataset.append(obj)
                
            # Write back to the same file
            with jsonlines.open(input_data, mode="w") as writer:
                writer.write_all(dataset)
                
            return dataset[0] if dataset else {}
    else:
        return {
            "radiant_heroes": input_data.get("RadiantHeroes", []),
            "dire_heroes": input_data.get("DireHeroes", []),
            "radiant_win": input_data.get("radiant_win", False)
        }

def process_heroes(input_file: str) -> None:
    """Process the heroes.json file by standardizing hero information format."""
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
        
    with open(input_file, 'r', encoding='utf-8') as fd:
        raw_data = json.load(fd)
        records = raw_data["constants"]["heroes"]
        
        # Process and standardize hero information
        heroes = [
            {
                "hero_id": hero["id"],
                "display_name": hero["displayName"],
                "name": hero["shortName"],
            }
            for hero in records.values()
        ]
        
    # Write back processed data
    with open(input_file, 'w', encoding='utf-8') as fd:
        json.dump({"heroes": heroes}, fd, indent=4)

def main() -> None:
    """Main function to orchestrate the data conversion process."""
    try:
        process_matches(MATCHES_FILE)
        process_heroes(HEROES_FILE)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
