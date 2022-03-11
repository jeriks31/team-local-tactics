from core import Champion, Match
from networking.common import parse_champion, stringify_champion


def _parse_match(matchText: str) -> tuple[str,str,int,int]:
    red_name, blue_name, red_score, blue_score = matchText.split(sep=',')
    return red_name, blue_name, red_score, blue_score


def load_champions() -> dict[str, Champion]:
    champions = {}
    with open('storage\\champions.csv', 'r') as file:
        for championText in file.readlines():
            champion = parse_champion(championText)
            champions[champion.name] = champion
    return champions


def load_matches() -> list[tuple[str,str,float,float]]:
    matches = []
    with open('storage\\matches.csv', 'r') as file:
        for matchText in file.readlines():
            match = _parse_match(matchText)
            matches.append(match)
    return matches


def save_champions(champions: dict[str, Champion]) -> None:
    with open('storage\\champions.csv', 'w') as file:
        stringified_champions = [stringify_champion(c) for c in champions.values()]
        file.writelines(stringified_champions)


def save_match(match: Match) -> None:
    with open('storage\\matches.csv', 'a') as file:
        red_name = match.red_team.name if len(match.red_team.name) > 0 else 'Red'
        blue_name = match.blue_team.name if len(match.blue_team.name) > 0 else 'Blue'
        red_score, blue_score = match.score()
        file.write(f'{red_name},{blue_name},{red_score},{blue_score}')