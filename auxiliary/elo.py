from typing import List
from typing_extensions import TypedDict
import random
import copy
import time

class Player(TypedDict):
    id: int
    name: str
    elo: float

def play(players: List[Player]) -> List[int]:
    # E_A = 1 / (1 + 10**((R_B - R_A) / 400))
    n = len(players)
    ranks = [1 for _ in range(n)]

    for i in range(n):
        for j in range(i+1, n):
            rank_1 = players[i].get('elo')
            rank_2 = players[j].get('elo')

            # Probability that player 1 wins player 2
            prob_1 = 1 / (1 + 10**((rank_2 - rank_1) / 400))

            if random.randrange(10**16) < prob_1 * 10**16:
                # Player 1 wins
                ranks[j] += 1
            else:
                # Player 2 wins
                ranks[i] += 1
    return ranks

def expected(players: List[Player]) -> List[float]:
    n = len(players)
    ranks = [1 for _ in range(n)]

    for i in range(n):
        for j in range(i+1, n):
            rank_1 = players[i].get('elo')
            rank_2 = players[j].get('elo')

            # Probability that player 1 wins player 2
            prob_1 = 1 / (1 + 10**((rank_2 - rank_1) / 400))

            ranks[j] += prob_1
            ranks[i] += 1 - prob_1
    
    return ranks

def update_rank(players: List[Player], ranks: List[int], expected_ranks: List[int]) -> List[Player]:
    new_players = []
    for i, player in enumerate(players):
        new_player = copy.copy(player)
        new_player['elo'] += 24 * (expected_ranks[i] - ranks[i])
        new_players.append(new_player)
    return new_players

if __name__ == '__main__':
    players = [Player(id=id, name=f'Player {id}', elo=1500) for id in range(1, 4+1)]

    turn = 1
    while True:
        ranks = play(players)
        expected_ranks = expected(players)

        print(turn, list(map(lambda player: round(player['elo']), players)))
        print(ranks, list(map(lambda r: int(r*1000)/1000, expected_ranks)))
        print()

        players = update_rank(players, ranks, expected_ranks)

        time.sleep(0.01)
        turn += 1