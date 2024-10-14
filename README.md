
# Premier League Fantasy Football Analysis

This project analyses data from the Fantasy Premier League (FPL) and provides visual insights into team performance using various metrics like points, rank, team value, transfers, and captain choices over the gameweeks. The data is fetched from the official FPL API, and a Streamlit app is built to visualise these metrics interactively.

Access the app here: https://fpl-fantasy-football.streamlit.app

## Features

- Fetches data directly from the Fantasy Premier League API.
- Displays team performance metrics such as points, rank, and value across gameweeks.
- Visualises team transfers, captain performance, and points distribution by position.
- Offers an interactive dashboard for team owners to monitor their team's progress over the season.

## Requirements

Make sure you have the following installed on your machine:

- Python 3.7+
- pip (Python package manager)

### Python Libraries
You can install the required libraries using the `requirements.txt` file provided:

```bash
pip install -r requirements.txt
```

The required libraries are:

- `streamlit`
- `plotly`
- `numpy`
- `pandas`
- `urllib3`
- `json`

## Getting Started

### Clone the Repository

To get a local copy of the project, run the following command:

```bash
git clone https://github.com/jrw22/fpl-app.git
cd fpl-app
```

### Running the Streamlit App

Once the repository is cloned and the required dependencies are installed, you can start the Streamlit app by running:

```bash
streamlit run streamlit_fpl_app.py
```

This will start the Streamlit app locally, and you can interact with the analysis in your web browser.

## Folder Structure

```
.
├── src/
|   └── Home.py                # Streamlit front-end
|   └── utils/                     
│       └── get_data.py        # Core function that pulls data from FPL API
├── requirements.txt           # List of Python dependencies
└── README.md                  # Project documentation
```

## Usage

1. **Fetch Data**: Data is fetched from the Fantasy Premier League API using the `get_data.py` script located in the `utils` folder.
2. **Visualisation**: The fetched data is visualised using plotly and integrated into the Streamlit app to display charts for metrics like team points, rank, transfers, and captain performance.
3. **Custom Configuration**: You can configure the team ID and the number of gameweeks to analyse directly in the `streamlit_fpl_app.py` file by updating the `team_id` and `last_gameweek` variables.

## API Usage

The project uses the Fantasy Premier League API to retrieve team and player data. You can adjust the `team_id` in the app to fetch data for any specific team.

## Example Visualisations

- **Team Points vs Average Points**: Compare your team’s weekly performance to the average and highest points.
- **Gameweek Rank**: Track your team’s gameweek and overall rank over the course of the season.
- **Transfers & Transfer Costs**: View the number of transfers made and their associated cost.
- **Captain Points**: Analyse the points scored by your selected captains.
- **Points Distribution**: See the breakdown of points by position (GK, DEF, MID, ST) (currently removed for bug fixing).


