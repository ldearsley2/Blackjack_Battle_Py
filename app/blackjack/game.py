import requests

from app.blackjack.card_manager import CardManager
from app.blackjack.player import Player
from app.services.game_service import GameService


class BlackJackGame:
    """
    BlackJackGame is responsible for maintaining game state.
    """

    def __init__(self, card_manager: CardManager, game_service: GameService):
        self.card_manager: CardManager = card_manager
        self.dealer_cards: list[str] = []
        self.dealer_stop: int = 17
        self.max_hand: int = 21
        self.players: list[Player] = []
        self.game_service: GameService = game_service

    def add_players(self):
        """
        Populate the game's players with those within the attached game manager
        """
        for player_id, url in self.game_service.connected_players.items():
            self.players.append(Player(player_id=str(player_id), url=url, points=10))

    def dealer_add_to_hand(self):
        """
        Add a card to the dealers hand
        """
        self.dealer_cards.append(self.card_manager.play_card())

    def deal_cards(self):
        """
        Starting point for a round, deal one card to dealer, two to each player.
        """
        self.dealer_add_to_hand()
        for p in self.players:
            for i in range(2):
                p.add_to_hand(self.card_manager.play_card())

    async def play_round(self):
        self.deal_cards()

        for player in self.players:
            json_req = {
                "player_id": player.player_id,
                "player_max_hand": str(self.max_hand),
                "dealer_stop": str(self.dealer_stop),
                "dealer_hand": self.dealer_cards,
                "current_hand": player.hand,
                "played_cards": self.card_manager.played_cards,
            }

            print(json_req)

            response = requests.post(url=f"{player.url}/turn", json=json_req)

            print(response.json)
