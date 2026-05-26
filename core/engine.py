import requests

class GameEngine:
    def __init__(self):
        self.data = {"score": 0}

    def get_crypto_price(self):
        try:
            # Fetches Bitcoin price in USD
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            response = requests.get(url).json()
            return float(response['bitcoin']['usd'])
        except:
            return 0.0

    def update_score(self):
        self.data["score"] += 1