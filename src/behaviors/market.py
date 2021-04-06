def behavior(state, context):

    '''
        state:
            sells: array of sell orders (messages)
            buys: array of buy orders (messages)
    '''
    if (state.counter == context.globals().steps):
        raise RuntimeError("_HASH_PRIVATE_TEMPORARY_COMPLETE_ERROR")
    
    props = context.globals()
    orders = context.messages()
    state.sells = [m for m in orders if m.type == "sell_order"] # update naming on sell limit
    state.buys = [m for m in orders if m.type == "buy_order"] # update naming on buy limit

    total_quantity_sold, total_quantity_bought = sum([m.data['quantity'] for m in sells]), sum([m.data['quantity'] for m in buys])

    def calculate_market_price_change(numbuys, numsells) -> int:
        print(numbuys, numsells)
        return numbuys, numsells

    while len(state.buys) > 0:
        while state.buys[0].data['quantity'] > 0 and len(state.sells) > 0:
            if state.sells[0].data["quantity"] == 0:
                state.addMessage(state.sells[0].agent, "results", {
                    "sell_order_remaining": state.sells[0].data["quantity"]
                })
                state.sells = state.sells[1:]
            if state.buys[0].data["quantity"] > state.sells[0].data["quantity"]:
                state.buys[0].data["quantity"] -= state.sells[0].data["quantity"]
                state.sells[0].data["quantity"] = 0
            else:
                state.buys[0].data["quantity"] = 0
                state.sells[0].data["quantity"] -= state.buys[0].data["quantity"]
        state.addMessage(state.buys[0].agent, "results", {
            "buy_order_remaining": state.buys[0].data["quantity"]
        })

    for sell_order in state.sells:
        state.addMessage(sell_order.agent, "results", {
            "sell_order_remaining": sell_order.data["quantity"]
        })
        
    context.globals().current_market_price = calculate_market_price_change(total_quantity_bought, total_quantity_sold)