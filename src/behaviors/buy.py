
import random
def behavior(state, context):
    bullish = context.globals()["confidence"] 

    buying = [m for m in context.messages() if m.type == "buy_results"]
    price_update = [m for m in context.messages() if m.type == "price_update"]
    original_price = context.globals()["initial_price"] 
    current_market_price = 20
    if len(price_update) > 0:
        # print(len(price_update))
        # print(price_update[0].type, price_update[0].to, price_update[0]["data"])
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
    

    # print("curr price = " + str(current_market_price))
    # print("orig price = "+ str(original_price))

    # print("buy = "+ str(state.buy_threshold * original_price))
    if state.capital > 0 and random.random() > bullish:
  # print("aboutta buy")
        state.add_message("market", "buy_order", {"quantity": 1})
        # int(state.capital / current_market_price)