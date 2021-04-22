def behavior(state, context):
    '''
        state:
            sells: array of sell orders (messages)
            buys: array of buy orders (messages)
    '''
    if (state.counter == context.globals()['steps']):
        raise RuntimeError("_HASH_PRIVATE_TEMPORARY_COMPLETE_ERROR")
    
    props = context.globals()
    orders = context.messages()
    
    state.sells = list(filter(lambda m: m.type == "sell_order", orders)) # update naming on sell limit
    state.buys = list(filter(lambda m: m.type == "buy_order", orders)) # update naming on buy limit
    total_quantity_sold, total_quantity_bought = 0, 0

    if len(state.sells) > 0:
        total_quantity_sold = sum([m.data["quantity"] for m in state.sells])
    if len(state.buys) > 0: 
        total_quantity_bought = sum([m.data["quantity"] for m in state.buys])

    def calculate_market_price_change(numbuys, numsells) -> float:
        # print("Number Buys: ", numbuys)
        # print("Number Sells: ", numsells)
        ratio = pow(1 + (numbuys / ((numsells + 1) * (props["starting_shares"]))), (numbuys - numsells))
        # print("Current price: ", state['current_price'])
        # print("New price: ", ratio * state['current_price'])
        return ratio * state['current_price']

    i, j = 0, 0
    
    while i < len(state.buys):
        state.add_message(state.buys[i]["from"], "buy_results", {
            "desired": state.buys[i].data["quantity"],
            "fulfilled": state.buys[i].data["quantity"],
            "price_fulfilled": state['current_price']
        })
        i += 1
    while j < len(state.sells):
        state.add_message(state.sells[j]["from"], "sell_results", {
            "desired": state.sells[j].data["quantity"],
            "fulfilled": state.sells[j].data["quantity"],
            "price_fulfilled": state['current_price']
        })
        j += 1
        
    prev_price = state['current_price']
    state['current_price'] = calculate_market_price_change(total_quantity_bought, total_quantity_sold)
    
    for i in range(props["retail_count"]):
        state.add_message("retail" + str(i), "price_update", {
            "current_price": state['current_price']
        })
    for i in range(props["hedge_count"]):
        state.add_message("hedge" + str(i), "price_update", {
            "current_price": state['current_price']
        })
    for i in range(props["wsb_count"]):
        state.add_message("wsb" + str(i), "price_update", {
            "current_price": state['current_price']
        })
    for i in range(props["melvin_count"]):
        state.add_message("melvin" + str(i), "price_update", {
            "current_price": state['current_price']
        })
    