import math
import random

# TODO: need to change function names
# we may not have to define the schema in context.globals, might be unnecessary if typing is consistent

def behavior(state, context):

    props = context.globals()
    market = {
        "agent_name": "market",
        "behaviors": ["@hash/counter/counter.rs", "market.py"],
        "counter": 0,
        "sells": [],
        "buys": []
    }
    retail_traders = [dict({
        "agent_type": "retail",
        "behaviors": ["@hash/counter/counter.rs", "sell.py", "buy.py"], # TODO: update the correct behaviors
        #"position": [i, 3],
        "shares": round(random.uniform(0, props["max_starting_shares"])),
        "counter": 0,
        "capital": props["retail_capital"],
        "profit_threshold": props["retail_profit"],
        "loss_threshold": props["retail_sell"],
        "buy_threshold": props["retail_buy"]
    }) for ind in range(int(props["retail_count"]))]

    wsb_traders = [dict({
        "agent_type": "wsb",
        "behaviors": ["@hash/counter/counter.rs", "sell.py", "buy.py"], # TODO: update the correct behaviors
        # "position": [i, 4],
        "shares": round(random.uniform(0, props["max_starting_shares"])),
        "counter": 0,
        "capital": props["wsb_capital"],
        "profit_threshold": props["wsb_profit"],
        "loss_threshold": props["wsb_sell"],
        "buy_threshold": props["wsb_buy"]
    }) for ind in range(int(props["wsb_count"]))]

    hedge_funds = [dict({
        "agent_type": "hedge",
        "behaviors": ["@hash/counter/counter.rs", "sell.py", "buy.py"], # TODO: update the correct behaviors
        #"position": [i, 5],
        "shorts": props["hedge_short_amount"],
        "counter": 0,
        # "price": 1,
        # "cost": 0,
        "capital": props["hedge_capital"],
        "profit_threshold": props["hedge_profit"],
        "loss_threshold": props["hedge_sell"],
        "buy_threshold": props["hedge_buy"]
    }) for ind in range(int(props["hedge_count"]))]

    melvin_funds = [dict({
        "agent_type": "melvin",
        "behaviors": ["@hash/counter/counter.rs", "sell.py", "buy.py"], # TODO: update the correct behaviors
        #"position": [i, 6],
        "shorts": props["melvin_short_amount"],
        "counter": 0,
        # "price": 1,
        # "cost": 0,
        "capital": props["melvin_capital"],
        "profit_threshold": props["melvin_profit"],
        "loss_threshold": props["melvin_sell"],
        "buy_threshold": props["melvin_buy"]
    }) for ind in range(int(props["melvin_count"]))]
    
    agents = retail_traders + wsb_traders + hedge_funds + melvin_funds + [market]
    for i, agent in enumerate(agents):
        state.add_message("hash", "create_agent", agent)
    state.add_message("hash", "remove_agent")
    