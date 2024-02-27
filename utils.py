# utils.py

def transform_data(data):
    transformed_data = {
        'nationalities': [],
        'championships': [],
        'teams': [],
        'players': [],
        'goals': [],
        'trophies': []
    }

    # Transform nationalities
    transformed_data['nationalities'] = [
        {'id': nationality['id'], 'name': nationality['name']} 
        for nationality in data.get('nationalities', [])
    ]

    # Transform championships
    transformed_data['championships'] = [
        {'id': champ['id'], 'name': champ['name'], 'nationality_id': champ['nationality_id']}
        for champ in data.get('championships', [])
    ]

    # Transform teams, players, and related entities
    for team_data in data.get('teams', []):
        team_id = team_data['id']

        # Transform team
        transformed_data['teams'].append({
            'id': team_id,
            'name': team_data['name'],
            'championship_id': team_data['championship_id']
            # Add other fields as needed
        })

        # Transform players
        for player_data in team_data.get('players', []):
            player_id = player_data['id']
            transformed_data['players'].append({
                'id': player_id,
                'name': player_data['name'],
                'surname': player_data['surname'],
                'number': player_data['number'],
                'nationality_id': player_data['nationality_id'],
                'team_id': team_id
                # Add other fields as needed
            })

            # Transform goals
            for goal_data in player_data.get('goals', []):
                transformed_data['goals'].append({
                    'id': goal_data['id'],
                    'player_id': player_id,
                    'match_type': goal_data['match_type'],
                    'count': goal_data['count']
                    # Add other fields as needed
                })

        # Transform trophies
        for trophy_data in team_data.get('best_player', {}).get('trophies', []):
            transformed_data['trophies'].append({
                'id': trophy_data['id'],
                'name': trophy_data['name'],
                'year': trophy_data['year'],
                'team_id': team_id
                # Add other fields as needed
            })

    return transformed_data
