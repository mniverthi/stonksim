
def behavior(state, context):

    buying = [m for m in context.messages() if m.type == "buy_results"]
    
    if len(buying) > 0:
        state.capital -= state.shares * context.globals()["current_market_price"] 
        state.behaviors=[]
        return
    

    
    if context.globals()["current_market_price"] < state.buy_threshold * context.globals()["original_market_price"]:
        state.addMessage("market", "buy_limit", {
        "sell_limit": state.buy_limit,
        "shares": state.shares,
        }) 
        