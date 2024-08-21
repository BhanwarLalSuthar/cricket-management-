import random


class Player:
    def __init__(self, name, age, role):
        self.name = name
        self.age = age
        self.role = role
        self.matches = 0
        self.runs = 0
        self.wickets = 0
        self.balls_faced = 0
        self.balls_bowled = 0
        self.runs_conceded = 0
        self.catches = 0
        self.run_outs = 0
        self.stumpings = 0
        self.dismissals = 0
        self.strike_rate = 0.0
        self.economy_rate = 0.0
        self.batting_average = 0.0
        self.bowling_average = 0.0
    
    def update_strike_rate(self):
        if self.balls_faced > 0:
            self.strike_rate = (self.runs / self.balls_faced) * 100
    
    def update_economy_rate(self):
        if self.balls_bowled > 0:
            self.economy_rate = self.runs_conceded / (self.balls_bowled / 6)

class Batsman(Player):
    def __init__(self, name, age):
        Player.__init__(self, name, age, role="Batsman")
    
    def update_batting_average(self):
        if self.dismissals > 0:
            self.batting_average = self.runs / self.dismissals

class Bowler(Player):
    def __init__(self, name, age):
        Player.__init__(self, name, age, role="Bowler")
    
    def update_bowling_average(self):
        if self.wickets > 0:
            self.bowling_average = self.runs_conceded / self.wickets

class AllRounder(Batsman, Bowler):
    def __init__(self, name, age):
        Player.__init__(self, name, age,role = "All-Rounder")
        self.batting_average = 0.0
        self.bowling_average = 0.0
       
    def update_batting_average(self):
        if self.dismissals > 0:
            self.batting_average = self.runs / self.dismissals
    
    def update_bowling_average(self):
        if self.wickets > 0:
            self.bowling_average = self.runs_conceded / self.wickets

class WicketKeeper(Batsman):
    def __init__(self, name, age):
        Batsman.__init__(self, name, age)
        self.role = "Wicket-Keeper"

# scoring algo
def calculate_runs_for_shot(shot_type):
    if shot_type == "leg_bye":
        return 1
    elif shot_type == "bye":
        return 0
    elif shot_type == "overthrow":
        return 4
    else:
        return int(shot_type)  # for normal shots like 1, 2, 4, 6

def calculate_runs_in_over(over_number, shot_type):
    base_runs = calculate_runs_for_shot(shot_type)
    if 1 <= over_number <= 6:  # Powerplay
        return base_runs * 1.2
    elif over_number > 40:  # Death overs
        return base_runs * 1.5
    else:
        return base_runs

def apply_penalties(ball_type, shot_type):
    penalty = 0
    if ball_type == "wide":
        penalty += 1
    elif ball_type == "no_ball":
        penalty += 1
    return penalty + calculate_runs_for_shot(shot_type)

def run_out_probability(distance_covered, reaction_time):
    if distance_covered > 30 and reaction_time > 2.0:
        return True
    return False


# match simulation
def simulate_over(batting_team, bowling_team, over_number):
    over_runs = 0
    over_wickets = 0
    for ball in range(6):
        shot_type = random.choice([1,2,3,4,5,6])
        ball_type = random.choice(["normal","wide","no_ball"])
        runs = apply_penalties(ball_type, shot_type)
        over_runs += runs

        # Simulate a wicket with a random chance
        wicket = False
        if random.choice([True, False]):
            wicket = True
            over_wickets += 1

        print(f"Runs scored: {runs}, Wicket: {wicket}")
    
    batting_team.runs += over_runs
    batting_team.wickets += over_wickets
    batting_team.overs += 1
    batting_team.runs_per_over.append(over_runs)
    print(f"Over {over_number} completed. Runs this over: {over_runs}. Wickets this over: {over_wickets}.\n")

def simulate_match(team_a, team_b, overs=2):
    print(f"Starting match between {team_a.name} and {team_b.name}")
    for over in range(1, overs+1):
        print(f"\n--- Over {over} ---")
        simulate_over(team_a, team_b, over)
    
    print(f"\n--- Innings Break ---\n{team_a.name} scored {team_a.runs} runs for {team_a.wickets} wickets in {team_a.overs} overs.\n")

    for over in range(1, overs+1):
        print(f"\n--- Over {over} ---")
        simulate_over(team_b, team_a, over)
    
    print(f"\n--- Match End ---\n{team_b.name} scored {team_b.runs} runs for {team_b.wickets} wickets in {team_b.overs} overs.\n")

    if team_a.runs > team_b.runs:
        print(f"{team_a.name} wins the match by {team_a.runs - team_b.runs} runs!")
    elif team_a.runs < team_b.runs:
        print(f"{team_b.name} wins the match by {team_b.runs - team_a.runs} runs!")
    else:
        print("The match is a tie!")


# team management
class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.runs = 0
        self.wickets = 0
        self.overs = 0
        self.runs_per_over = []  # List to store runs per over
    
    def add_player(self, player):
        self.players.append(player)
    
    def remove_player(self, player):
        self.players.remove(player)

def compare_players(player1, player2, metric):
    if metric == "batting_average":
        return player1.batting_average > player2.batting_average
    elif metric == "bowling_average":
        return player1.bowling_average < player2.bowling_average
    # Add more comparison metrics as needed


# data visualization

import matplotlib.pyplot as plt


def plot_runs_per_over(team_a, team_b, total_overs):
    overs = list(range(1, total_overs + 1))
    
    # Ensure both lists have the same length as total_overs
    team_a_runs = team_a.runs_per_over + [0] * (total_overs - len(team_a.runs_per_over))
    team_b_runs = team_b.runs_per_over + [0] * (total_overs - len(team_b.runs_per_over))
    
    plt.plot(overs, team_a_runs, label=team_a.name, marker='o')
    plt.plot(overs, team_b_runs, label=team_b.name, marker='o')
    plt.xlabel('Overs')
    plt.ylabel('Runs')
    plt.title('Runs per Over')
    plt.legend()
    plt.show()

def plot_batting_average(players):
    names = [player.name for player in players]
    averages = [player.batting_average for player in players]
    plt.bar(names, averages)
    plt.xlabel('Player')
    plt.ylabel('Batting Average')
    plt.title('Batting Averages')
    plt.show()

def plot_bowling_average(players):
    names = [player.name for player in players]
    averages = [player.bowling_average for player in players]
    plt.bar(names, averages)
    plt.xlabel('Player')
    plt.ylabel('Bowling Average')
    plt.title('Bowling Averages')
    plt.show()




team_a = Team(name="Team A")
team_b = Team(name="Team B")

# Add Players to Teams
team_a.add_player(Batsman(name="Player A1", age=30))
team_a.add_player(Bowler(name="Player A2", age=28))
team_a.add_player(AllRounder(name="Player A3", age=27))
team_a.add_player(WicketKeeper(name="Player A4", age=29))

team_b.add_player(Batsman(name="Player B1", age=31))
team_b.add_player(Bowler(name="Player B2", age=26))
team_b.add_player(AllRounder(name="Player B3", age=28))
team_b.add_player(WicketKeeper(name="Player B4", age=30))

# Simulate the Match
simulate_match(team_a, team_b, overs=2)

plot_runs_per_over(team_a, team_b, total_overs=2)
