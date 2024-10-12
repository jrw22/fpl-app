# Import necessary packages
import json
import urllib.request

def get_team_general_info(team_id):
    """
    Fetches general information about the team based on the team ID.

    Args:
        team_id (int): The ID of the team.

    Returns:
        dict: Dictionary containing the team's general information.
    """
    try:
        base = f"https://fantasy.premierleague.com/api/entry/{team_id}/"
        page = urllib.request.urlopen(base)
        team_info_data = json.load(page)
        return team_info_data
    except Exception as e:
        print(f"Error fetching team general info: {e}")
        return None

def get_team_gw_info(last_gameweek, team_id):
    """
    Fetches detailed information for each gameweek of the team.

    Args:
        last_gameweek (int): The last gameweek for which data is needed.
        team_id (int): The ID of the team.

    Returns:
        dict: Dictionary with gameweek-specific data for the team.
    """
    try:
        gameweek_data = {}
        for i in range(1, last_gameweek + 1):
            base = f"https://fantasy.premierleague.com/api/entry/{team_id}/event/{i}/picks/"
            page = urllib.request.urlopen(base)
            data = {f"GW{i}": json.load(page)}
            gameweek_data.update(data)
        return gameweek_data
    except Exception as e:
        print(f"Error fetching gameweek info: {e}")
        return None

def get_premier_league_info():
    """
    Fetches general updates about the Premier League, including team and player information.

    Returns:
        dict: Dictionary containing Premier League-wide data.
    """
    try:
        base = "https://fantasy.premierleague.com/api/bootstrap-static/"
        page = urllib.request.urlopen(base)
        data_general = json.load(page)
        return data_general
    except Exception as e:
        print(f"Error fetching Premier League info: {e}")
        return None

def get_player_points_one_gw(player_id, gameweek):
    """
    Fetches the points a player scored in a specific gameweek.

    Args:
        player_id (int): The ID of the player.
        gameweek (int): The gameweek number.

    Returns:
        int: Points scored by the player in the specified gameweek.
    """
    try:
        base = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
        page = urllib.request.urlopen(base)
        datagw = json.load(page)
        
        # Accumulate points in case of double gameweeks
        gw_points = 0
        for gw_data in datagw["history"]:
            if gameweek == gw_data["round"]:
                gw_points += gw_data["total_points"]

        return gw_points
    except Exception as e:
        print(f"Error fetching player points for gameweek {gameweek}: {e}")
        return 0

def get_player_name(player_id, elements):
    """
    Fetches the full name of a player based on their player ID.

    Args:
        player_id (int): The ID of the player.
        elements (list): List of all player data from the API.

    Returns:
        str: Full name of the player or 'ID not found' if not found.
    """
    try:
        for element in elements:
            if element["id"] == player_id:
                return f"{element['first_name']} {element['second_name']}"
        return "ID not found"
    except Exception as e:
        print(f"Error fetching player name for ID {player_id}: {e}")
        return "ID not found"

def get_player_position(player_id, elements):
    """
    Fetches the position of a player based on their player ID.

    Args:
        player_id (int): The ID of the player.
        elements (list): List of all player data from the API.

    Returns:
        str: The position of the player (GK, DEF, MID, ST) or 'ID not found' if not found.
    """
    positions = ["GK", "DEF", "MID", "ST"]
    try:
        for element in elements:
            if element["id"] == player_id:
                return positions[element["element_type"] - 1]
        return "ID not found"
    except Exception as e:
        print(f"Error fetching player position for ID {player_id}: {e}")
        return "ID not found"

# Main data extraction function
def get_data(team_id, last_gameweek):
    """
    Fetches and aggregates data for a given team up to the specified gameweek.

    Args:
        team_id (int): The ID of the team.
        last_gameweek (int): The last gameweek for which data is needed.

    Returns:
        tuple: Aggregated data for the team including points, ranks, transfers, etc.
    """
    try:
        team_info_data = get_team_general_info(team_id)
        if not team_info_data:
            return None

        team_name = team_info_data["name"]
        gameweek_data = get_team_gw_info(last_gameweek, team_id)
        data_general = get_premier_league_info()
        elements = data_general["elements"]

        # Initialise lists to store data for each gameweek
        points, gameweek_rank, overall_rank, team_value, transfers, transfers_cost = [], [], [], [], [], []
        average_points, highest_points, captain, captain_points = [], [], [], []
        total_points_per_line_season = {"GK": 0, "DEF": 0, "MID": 0, "ST": 0}

        # Process each gameweek
        for gw in range(1, last_gameweek + 1):
            gw_data = gameweek_data[f"GW{gw}"]["entry_history"]
            points.append(gw_data["points"])
            gameweek_rank.append(gw_data["rank"])
            overall_rank.append(gw_data["overall_rank"])
            team_value.append(gw_data["value"])
            transfers.append(gw_data["event_transfers"])
            transfers_cost.append(gw_data["event_transfers_cost"])
            average_points.append(data_general["events"][gw - 1]["average_entry_score"])
            highest_points.append(data_general["events"][gw - 1]["highest_score"])

            # Identify captain and collect captain points
            for player in gameweek_data[f"GW{gw}"]["picks"]:
                if player["is_captain"]:
                    captain.append(get_player_name(player["element"], elements))
                    captain_points.append(get_player_points_one_gw(player["element"], gw))

        print("Data retrieved successfully")
        return team_name, points, average_points, highest_points, gameweek_rank, overall_rank, team_value, transfers, transfers_cost, captain, captain_points, total_points_per_line_season
    
    except Exception as e:
        print(f"Error retrieving data for team {team_id}: {e}")
        return None