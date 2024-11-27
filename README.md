# Game Oracle: A High-Level Dota 2 Match Dataset

## Executive Summary

Game Oracle is a comprehensive dataset of high-level Dota 2 matches, designed to provide insights into professional and high-ranked player strategies and decision-making. This dataset includes detailed match information from top-ranked players on official leaderboards across different regions (Americas, SE Asia, Europe, and China).

### Motivation
The esports industry, particularly Dota 2, lacks accessible, high-quality datasets focusing on high-level gameplay. This dataset aims to bridge this gap by providing researchers and analysts with rich data about hero selections, bans, and match outcomes from top-tier players.

### Potential Applications
- Predictive modeling for draft strategies
- Analysis of meta trends in professional Dota 2
- Player behavior and decision-making research
- Game balance analysis
- Esports betting and analytics

## Description of Data

The dataset contains:
- Match data from top-ranked players across all major regions
- Hero picks and bans for each match
- Match outcomes and basic statistics
- Player ranks and regional information

### Data Format
- `matches.jsonl`: Contains detailed match information
- `heroes.json`: Reference data for all Dota 2 heroes

## Power Analysis Results
The dataset includes matches from the top 100 players from each region's leaderboard, ensuring a statistically significant sample size for analyzing high-level gameplay patterns. Each hero appears in multiple matches, providing robust data for win rate and pick rate analysis.

## Exploratory Data Analysis

Key findings from our analysis:
1. Hero Pick Rates: Analysis of most picked heroes at high-level play
2. Ban Rates: Most banned heroes in competitive matches
3. Win Rates: Hero performance statistics
4. Regional Variations: Differences in hero preferences across regions

Detailed visualizations can be found in the `EDA` directory.

## Data Collection Code

The data collection pipeline consists of several Python scripts:

1. `get_players.py`: Fetches player data from STRATZ API
2. `get_matches_by_player.py`: Retrieves match data for selected players
3. `parse_matches.py`: Processes and cleans match data
4. `convert_to_public_dataset.py`: Prepares data for public release

## Ethics Statement

This dataset:
- Uses only publicly available match data
- Respects player privacy by focusing on gameplay data rather than personal information
- Acknowledges potential regional biases in player representation
- Is collected through official API channels, following all terms of service
- Aims to promote fair and ethical analysis of competitive gaming

## License

The code is licensed under the Creative Commons Attribution-NonCommercial (CC BY-NC) License. See the [CODE_LICENSE](CODE_LICENSE) file for details.

The dataset is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License - see the [DATA_LICENSE](DATA_LICENSE) file for details.

## Setup and Usage

### Requirements
```bash
pip install -r requirements.txt
```

### Running the Code
1. Go to https://stratz.com/api and sign up for an API key. Then set the
   `STRATZ_API_KEY` environment variable to the key you received. 
   
2. Run data collection pipeline:
   ```bash
   python get_players.py
   python get_matches_by_player.py
   python parse_matches.py
   ```
3. Run EDA:
   ```bash
   python EDA/EDA.py
   ```

### Unit Tests

```bash
pytest
```