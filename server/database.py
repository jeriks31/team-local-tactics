def load_champions():
    champions = []
    with open("data/champions.csv", "r") as db:
        for champ_text in db.readlines():
            name, rock, paper, scissors = champ_text.split(sep=",")
            champions.append(Champion(name, float(rock), float(paper), float(scissors)))
    return champions

def save_match(match, time):
    for round in match.rounds():
        for champion_names, throw in round.items():


def load_match_history(champion):
    pass