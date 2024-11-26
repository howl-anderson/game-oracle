# Game Oracle

A data pipeline project for collecting and processing game-related data.

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Install dependencies

```bash
pip install -r requirements.txt
```


## Data Pipeline

### 1. Get Player Data
Run the player data collection script:
```bash
python get_players.py
```

### 2. Get Match Data
Collect match data for players:
```bash
python get_matches_by_player.py
```

### 3. Parse Match Data
Process and parse the collected match data:
```bash
python parse_matches.py
```

### 4. Convert to Public Dataset
Convert the parsed match data to a public dataset:
```bash
python convert_to_public_dataset.py
```

## Testing

Run the test suite using pytest:
```bash
pytest
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.