import logging

logging.basicConfig(filename='trades.log', level=logging.INFO)

def log_trade(action, price, amount):
    logging.info(f"{action} at {price} for {amount}")
