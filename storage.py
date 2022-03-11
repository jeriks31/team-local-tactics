from core import Champion, Match
from parsing import parse_champions, serialize_champions, parse_match, serialize_match

DIR = 'storage'

def load_champions() -> dict[str, Champion]:
    with open(f'{DIR}\\champions.csv', 'r') as file:
        return parse_champions('\n'.join(file.readlines()))

def load_matches() -> list[tuple[str,str,float,float]]:
    matches = []
    with open(f'{DIR}\\matches.csv', 'r') as file:
        for matchText in file.readlines():
            matches.append(parse_match(matchText))
    return matches

def save_champions(champions: dict[str, Champion]) -> None:
    with open(f'{DIR}\\champions.csv', 'w') as file:
        file.write(serialize_champions(champions))

def save_match(match: Match) -> None:
    with open(f'{DIR}\\matches.csv', 'a') as file: 
        file.write(serialize_match(match) + '\n')