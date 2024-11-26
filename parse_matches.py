"""
This module parses raw Dota 2 match data from JSON files and converts it into a structured format.
"""

from typing import List, Dict, Any
import json
from pathlib import Path
from dataclasses import dataclass

import jsonlines
from tqdm import tqdm

# Constants
INPUT_DIR = "players_matches"
OUTPUT_FILE = "matches.jsonl"

@dataclass
class MatchData:
    """Data structure for storing match information."""
    match_id: int
    radiant_win: bool
    radiant_heroes: List[int]
    dire_heroes: List[int]
    radiant_bans: List[int]
    dire_bans: List[int]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the match data to a dictionary format."""
        return {
            "match_id": self.match_id,
            "radiant_win": self.radiant_win,
            "RadiantHeroes": self.radiant_heroes,
            "DireHeroes": self.dire_heroes,
            "RadiantBanedHeroes": self.radiant_bans,
            "DireBanedHeroes": self.dire_bans,
        }

def parse_single_file(match_file: Path) -> List[Dict[str, Any]]:
    """Parse a single match data file and extract relevant information."""
    try:
        with open(match_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        result = []
        
        for player in data["players"]:
            for match in player["matches"]:
                if not match.get("pickBans"):
                    continue
                    
                match_data = MatchData(
                    match_id=match["id"],
                    radiant_win=match["didRadiantWin"],
                    radiant_heroes=[],
                    dire_heroes=[],
                    radiant_bans=[],
                    dire_bans=[]
                )
                
                for pick_ban in match["pickBans"]:
                    if not isinstance(pick_ban.get("isPick"), bool):
                        continue
                        
                    hero_id = pick_ban.get("heroId")
                    if not hero_id:
                        continue
                        
                    if pick_ban["isPick"]:
                        if pick_ban["isRadiant"]:
                            match_data.radiant_heroes.append(hero_id)
                        else:
                            match_data.dire_heroes.append(hero_id)
                    else:
                        if pick_ban["isRadiant"]:
                            match_data.radiant_bans.append(hero_id)
                        else:
                            match_data.dire_bans.append(hero_id)
                
                result.append(match_data.to_dict())
                
        return result
        
    except Exception as e:
        print(f"Error processing file {match_file}: {str(e)}")
        return []

def process_match_files(input_dir: str, output_file: str) -> None:
    """Process all match files in the input directory and save results to output file."""
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
    json_files = list(input_path.glob("*.json"))
    if not json_files:
        raise ValueError(f"No JSON files found in {input_dir}")
        
    records = []
    
    for json_file in tqdm(json_files, desc="Processing match files"):
        file_records = parse_single_file(json_file)
        records.extend(file_records)
        
    print(f"Processed {len(records)} matches from {len(json_files)} files")
    
    with jsonlines.open(output_file, mode='w') as writer:
        writer.write_all(records)

def main() -> None:
    """Main function to orchestrate the match data processing pipeline."""
    try:
        process_match_files(INPUT_DIR, OUTPUT_FILE)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
