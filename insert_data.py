# insert_data.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from db_schema import Base, Nationality, Championship, Team, Player, Goal, Trophy

# Create an SQLite database in memory for testing
engine = create_engine('sqlite:///soccer.db')
Base.metadata.create_all(engine)  # Ensure tables are created

Session = sessionmaker(bind=engine)
session = Session()

def insert_data(data):
    # Insert data into the database
    for nationality_data in data['nationalities']:
        nationality = Nationality(**nationality_data)
        session.add(nationality)

    for championship_data in data['championships']:
        championship = Championship(**championship_data)
        session.add(championship)

    for team_data in data['teams']:
        # Extract the best_player data
        best_player_data = team_data.pop('best_player', {})

        # Insert team without the best_player field
        team = Team(**team_data)
        session.add(team)

        # Insert best_player as a separate player
        best_player = Player(
            name=best_player_data.get('name'),
            surname=best_player_data.get('surname'),
            number=best_player_data.get('number'),
            nationality_id=best_player_data.get('nationality_id'),
            team=team  # Associate the player with the team
        )
        session.add(best_player)

        # Insert goals for best_player
        for goal_data in best_player_data.get('goals', []):
            goal = Goal(
                player=best_player,  # Associate the goal with the player
                match_type=goal_data.get('match_type'),
                count=goal_data.get('count')
            )
            session.add(goal)

        # Insert trophies for best_player
        for trophy_data in best_player_data.get('trophies', []):
            trophy = Trophy(
                name=trophy_data.get('name'),
                year=trophy_data.get('year'),
                team=team  # Associate the trophy with the team
            )
            session.add(trophy)

    session.commit()
    session.close()

if __name__ == "__main__":
    # Load JSON data
    with open('teams.json', 'r') as file:
        data = json.load(file)
        print(data)  # Add this line to print the loaded data
    
    # Insert data into the database
    insert_data(data)
