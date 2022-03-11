from core import Champion, Match

# Champion

def parse_champion(championText: str) -> Champion:
    """Parse a CSV champion."""
    name, rock, paper, scissors = championText.split(sep=',')
    return Champion(name, float(rock), float(paper), float(scissors))

def serialize_champion(champion: Champion) -> str:
    """Serialize a champion to CSV."""
    return ",".join(champion.str_tuple)

# Champions

def parse_champions(championsText: str) -> dict[str, Champion]:
    """Parse a CSV list of champions."""
    champions = {}
    for championText in championTexts.split('\n'):
        champion = parse_champion(championText)
        champions[champion.name] = champion
    return champions

def serialize_champions(champions: dict[str, Champion]) -> str:
    """Serialize a dictionary of champions to CSV."""
    return '\n'.join([stringify_champion(champion) for champion in list(champions.values())])

# Matches

def parse_match(matchText:str) -> tuple[str,str,int,int]:
    red_name, blue_name, red_score, blue_score = matchText.split(sep=',')
    return red_name, blue_name, red_score, blue_score

def serialize_match(match:Match) -> str:
    red_name = match.red_team.name if len(match.red_team.name) > 0 else 'Red'
    blue_name = match.blue_team.name if len(match.blue_team.name) > 0 else 'Blue'
    red_score, blue_score = match.score()
    return f'{red_name},{blue_name},{red_score},{blue_score}'