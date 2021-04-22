import random

def behavior(state, context):

    props = context.globals()

    buying = [m for m in context.messages() if m.type == "buy_results"]
    price_update = [m for m in context.messages() if m.type == "price_update"]
    original_price = context.globals()["initial_price"] 
    current_market_price = original_price

    if len(price_update) > 0:
        if (len(price_update[0]["data"]) > 0):
            current_market_price = price_update[0]["data"]["current_price"]
    
    if len(buying) > 0:
        price_fulfilled = buying[0]["data"]["price_fulfilled"]
        shares_bought = sum([m["data"]["desired"] for m in buying])
        state.shares += shares_bought
        state.capital -= shares_bought * price_fulfilled
        if state.capital == 0 and state.shares == 0:
            state.behaviors = []
            return

    if state.counter % props["time_to_cover"] == 0 and random.random() < props["short_interest"]:
        state.add_message("market", "buy_order", {"quantity": 10})