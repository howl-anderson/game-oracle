"""
Analysis of hero pick rates, ban rates, and win rates in Dota 2 matches.

This script processes match data to generate and visualize statistics about hero usage patterns,
including pick rates, ban rates, and win rates. The results are saved as PNG files.
"""

import collections
from pathlib import Path
import json
import jsonlines
import pandas as pd
import matplotlib.pyplot as plt

# Constants
CURRENT_DIR = Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent

def load_matches(data_dir):
    """Load match data from jsonlines file."""
    matches = []
    with jsonlines.open(data_dir / "matches.jsonl") as reader:
        for obj in reader:
            matches.append(obj)
    return matches

def load_heroes(data_dir):
    """Load hero data from JSON file and create a hero_id to hero mapping."""
    with open(data_dir / "heroes.json", "r") as f:
        raw_heroes = json.load(f)
    return {hero["hero_id"]: hero for hero in raw_heroes}

def calculate_hero_statistics(matches):
    """Calculate win, loss, and ban statistics for each hero."""
    usage_stats = collections.defaultdict(lambda: {"lose": 0, "win": 0, "ban": 0})
    
    for match in matches:
        # Process wins and losses
        winners = match["RadiantHeroes"] if match["radiant_win"] else match["DireHeroes"]
        losers = match["DireHeroes"] if match["radiant_win"] else match["RadiantHeroes"]
        
        for hero in winners:
            usage_stats[hero]["win"] += 1
        for hero in losers:
            usage_stats[hero]["lose"] += 1
            
        # Process bans
        for hero in match["RadiantBanedHeroes"] + match["DireBanedHeroes"]:
            usage_stats[hero]["ban"] += 1
            
    return usage_stats

def create_hero_dataframe(usage_stats, heroes):
    """Create a pandas DataFrame with hero statistics."""
    data = []
    for hero_id, stats in usage_stats.items():
        total_games = stats["win"] + stats["lose"]
        data.append({
            "hero_name": heroes[hero_id]["name"],
            "count": total_games,
            "baned_count": stats.get("ban", 0),
            "win_rate": stats["win"] / total_games if total_games > 0 else 0
        })
    
    df = pd.DataFrame(data)
    
    # Calculate rates
    df["usage_rate"] = df["count"] / df["count"].sum()
    df["ban_rate"] = df["baned_count"] / df["baned_count"].sum()
    
    return df

def plot_hero_statistics(df, metric, output_path, add_baseline=False):
    """Plot and save hero statistics."""
    plt.figure(figsize=(20, 5))
    df_sorted = df.sort_values(by=metric, ascending=False)
    ax = df_sorted.plot(kind="bar", x="hero_name", y=metric, figsize=(20, 5))
    
    # Rotate labels 90 degrees
    plt.xticks(rotation=90)
    
    if add_baseline:
        plt.axhline(y=0.5, color="r", linestyle="-")
    
    plt.tight_layout()  # Automatically adjust layout to prevent label clipping
    plt.savefig(output_path, bbox_inches='tight')  # Ensure no labels are clipped when saving
    plt.close()

def main():
    # Load data
    matches = load_matches(DATA_DIR)
    heroes = load_heroes(DATA_DIR)
    
    # Process data
    usage_stats = calculate_hero_statistics(matches)
    hero_df = create_hero_dataframe(usage_stats, heroes)
    
    # Generate plots
    plot_hero_statistics(hero_df, "usage_rate", CURRENT_DIR / "heroes_pick_distribution.png")
    plot_hero_statistics(hero_df, "ban_rate", CURRENT_DIR / "heroes_ban_distribution.png")
    plot_hero_statistics(hero_df, "win_rate", CURRENT_DIR / "heroes_winrate_distribution.png", 
                        add_baseline=True)

if __name__ == "__main__":
    main()