import random

def behavior(state, context):
    
    selling = [m for m in context.messages() if m.type == "sell_results"]
    price_update = [m for m in context.messages() if m.type == "price_update"]
    original_price = context.globals()["initial_price"] 
    current_market_price = original_price
    
    if len(price_update) > 0:
        if (len(price_update[0]["data"]) > 0):
            current_market_price = price_update[0]["data"]["current_price"]
    
    if len(selling) > 0:
        price_fulfilled = selling[0]["data"]["price_fulfilled"]
        shares_sold = sum([m["data"]["desired"] for m in selling])
        state.shares -= shares_sold
        state.capital += shares_sold * price_fulfilled
        if state.shares == 0 and state.capital == 0:
            state.behaviors = []
            return
    
    if state.shares > 0 and random.random() < state["sell_threshold"]:
        state.add_message("market", "sell_order", {"quantity": 1})