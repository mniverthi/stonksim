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

    # print(orders)
    
    state.sells = list(filter(lambda m: m.type == "sell_order", orders)) # update naming on sell limit
    state.buys = list(filter(lambda m: m.type == "buy_order", orders)) # update naming on buy limit
    total_quantity_sold, total_quantity_bought = 0, 0
    if len(state.sells) > 0:
        # for i in state.sells:
        #     print(len(i["data"]))
        total_quantity_sold = sum([m.data["quantity"] for m in state.sells])
    if len(state.buys) > 0:    
        total_quantity_bought = sum([m.data["quantity"] for m in state.buys])

    def calculate_market_price_change(numbuys, numsells) -> float:
        if numsells == 0 and numbuys == 0:
            return state['current_price']
        if numsells == 0:
            numsells = 1
        ratio = 0.2 * (numbuys - numsells)
        return int(state['current_price']) + ratio

    i, j = 0, 0
    while i < len(state.buys) and j < len(state.sells):
        if state.buys[i].data['quantity'] > state.sells[j].data['quantity']:
            state.add_message(state.sells[j]["from"], "sell_results", {
                "desired": state.sells[j].data["quantity"],
                "fulfilled": 0,
                "price_fulfilled": state['current_price']
            })
            state.buys[i].data["quantity"] -= state.sells[j].data["quantity"]
            state.sells[j].data["quantity"] = 0
            j += 1
        elif state.buys[i].data['quantity'] < state.sells[j].data['quantity']:
            state.add_message(state.buys[i]["from"], "buy_results", {
                "desired": state.buys[i].data["quantity"],
                "fulfilled": 0,
                "price_fulfilled": state['current_price']
            })
            state.sells[j].data["quantity"] -= state.buys[i].data["quantity"]
            state.buys[i].data["quantity"] = 0
            i += 1
        else:
            state.add_message(state.sells[j]["from"], "sell_results", {
                "desired": state.sells[j].data["quantity"],
                "fulfilled": 0,
                "price_fulfilled": state['current_price']
            })
            state.add_message(state.buys[i]["from"], "buy_results", {
                "desired": state.buys[i].data["quantity"],
                "fulfilled": 0,
                "price_fulfilled": state['current_price']
            })
            state.buys[i].data["quantity"] = 0
            state.sells[j].data["quantity"] = 0
            i += 1
            j += 1
    
    while i < len(state.buys):
        state.add_message(state.buys[i]["from"], "buy_results", {
            "desired": state.buys[i].data["quantity"],
            "fulfilled": 0,
            "price_fulfilled": state['current_price']
        })
        i += 1
    while j < len(state.sells):
        state.add_message(state.sells[j]["from"], "sell_results", {
            "desired": state.sells[j].data["quantity"],
            "fulfilled": 0,
            "price_fulfilled": state['current_price']
        })
        j += 1
        
    prev_price = state['current_price']
    state['current_price'] = calculate_market_price_change(total_quantity_bought, total_quantity_sold)
    print("Previous price: ", prev_price)
    print("Current price: ", state['current_price'])
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
    