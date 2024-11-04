import json
import os
import math

# Function to load fixture data from JSON file
def load_fixture_data(file_path):
    with open(file_path, 'r') as file:
        fixtures = json.load(file)
    return fixtures

# Function to calculate standard deviation
def calculate_standard_deviation(values):
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return math.sqrt(variance)

# Prediction algorithm considering home_team, away_team, and head_to_head data
def make_prediction(fixture):
    prediction = {
        "cards": {
            "discuss": "",
            "ht": predict_cards_ht(fixture),
            "ft": predict_cards_ft(fixture)
        },
        "corners": {
            "discuss": "",
            "full_time_total_corners": predict_corners_ft(fixture),
            "1x2_corners": predict_corners_1x2(fixture)
        },
        "goals": {
            "discuss": "",
            "Both_teams_to_score": predict_both_teams_to_score(fixture),
            "fulltime_total_goals": predict_total_goals(fixture)
        },
        "1x_x2": {
            "discuss": "",
            "win_or_draw": predict_win_or_draw(fixture)
        }
    }
    return prediction

# Helper prediction functions
def predict_cards_ht(fixture):
    # Calculate average and standard deviation for half-time cards
    ht_cards = [card for match in fixture['head_to_head']['HT_cards'].values() for card in match]
    average_ht_cards = sum(ht_cards) / len(ht_cards)
    std_dev_ht_cards = calculate_standard_deviation(ht_cards)
    yellow_per_game = fixture['referee']['yellow_per_game']

    if average_ht_cards > 1.5 and std_dev_ht_cards > 3 and yellow_per_game > 3.5:
        return "Over 1.5 cards"
    elif average_ht_cards < 1.5 and std_dev_ht_cards < 3:
        return "Under 2.5 cards"
    else:
        return "No Prediction"

def predict_cards_ft(fixture):
    # Calculate average and standard deviation for full-time cards
    ft_cards = [card for match in fixture['head_to_head']['FT_cards'].values() for card in match]
    average_ft_cards = sum(ft_cards) / len(ft_cards)
    std_dev_ft_cards = calculate_standard_deviation(ft_cards)
    yellow_per_game = fixture['referee']['yellow_per_game']

    if average_ft_cards > 3.5 and std_dev_ft_cards > 2 and yellow_per_game > 3.5:
        return "Over 3.5 cards"
    elif average_ft_cards < 4.5 and std_dev_ft_cards < 2:
        return "Under 5.5 cards"
    elif average_ft_cards > 2.5 and std_dev_ft_cards > 1:
        return "Over 2.5 cards"
    else:
        return "No Prediction"

def predict_corners_ft(fixture):
    # Calculate average and standard deviation for full-time corners
    corner_totals = [sum(match) for match in fixture['head_to_head']['corners'].values()]
    combined_avg_corners = sum(corner_totals) / len(corner_totals)
    std_dev_corners = calculate_standard_deviation(corner_totals)

    if combined_avg_corners < 8 and std_dev_corners < 4:
        return "Under 12.5 corners"
    elif combined_avg_corners < 8:
        return "Under 11.5 corners"
    elif combined_avg_corners > 8 and std_dev_corners > 3:
        return "Over 8.5 corners"
    else:
        return "Over 12.5 corners"

def predict_corners_1x2(fixture):
    home_corners = sum([match[0] for match in fixture['head_to_head']['corners'].values()])
    away_corners = sum([match[1] for match in fixture['head_to_head']['corners'].values()])
    return "Home_team" if home_corners > away_corners else "Away_team"

def predict_both_teams_to_score(fixture):
    both_teams_score = [1 if match[0] > 0 and match[1] > 0 else 0 for match in fixture['head_to_head']['goals'].values()]
    return "Yes" if sum(both_teams_score) / len(both_teams_score) > 0.5 else "No"

def predict_total_goals(fixture):
    goal_values = [sum(match) for match in fixture['head_to_head']['goals'].values()]
    avg_goals = sum(goal_values) / len(goal_values)
    std_dev_goals = calculate_standard_deviation(goal_values)

    if avg_goals > 3.5 and std_dev_goals > 2:
        return "O 3.5"
    elif avg_goals > 2.5 and std_dev_goals > 1:
        return "O 2.5"
    elif avg_goals < 2 and std_dev_goals < 2:
        return "U 3.5"
    else:
        return "U 4.5" if avg_goals < 4.5 else "O 4.5"

def predict_win_or_draw(fixture):
    home_wins = sum([1 if match[0] > match[1] else 0 for match in fixture['head_to_head']['goals'].values()])
    away_wins = sum([1 if match[1] > match[0] else 0 for match in fixture['head_to_head']['goals'].values()])
    recent_home_performance = sum([1 if match[0] > match[1] else 0 for match in fixture['home_team']['recent_matches']['goals'].values()])
    recent_away_performance = sum([1 if match[1] > match[0] else 0 for match in fixture['away_team']['recent_matches']['goals'].values()])
    return "Home_team" if home_wins + recent_home_performance > away_wins + recent_away_performance else "Away_team"

# Function to save prediction for each fixture
def save_prediction(prediction, fixture_name):
    if not os.path.exists("predictions"):
        os.makedirs("predictions")
    file_path = os.path.join("predictions", f"{fixture_name.replace(' ', '_')}_prediction.json")
    with open(file_path, 'w') as file:
        json.dump(prediction, file, indent=4)

# Main function to run the algorithm
def run_prediction_algorithm(fixture_file_path):
    fixtures = load_fixture_data(fixture_file_path)
    for fixture in fixtures:
        prediction = make_prediction(fixture)
        save_prediction(prediction, fixture['fixture'])

# Path to the fixture JSON file
fixture_file_path = 'eredivisie.json'

# Run the prediction algorithm
run_prediction_algorithm(fixture_file_path)
