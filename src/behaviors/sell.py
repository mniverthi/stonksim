def behavior(state, context):

    sale = [m for m in context.messages() if m.type == "sell_results"]
    
    if len(sale) > 0:
        state.capital += state.shares * context.globals()["current_market_price"] 
        state.shares = 0
        state.behaviors=[]
        return
    

    
    if context.globals()["current_market_price"] > state.profit_threshold * context.globals()["original_market_price"]\
    or context.globals()["current_market_price"] < state.loss_threshold * context.globals()["original_market_price"]:
        state.add_message("market", "sell_limit", {
        "sell_limit": state.sell_limit,
        "shares": state.shares,
        }) 