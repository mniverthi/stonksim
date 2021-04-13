def behavior(state, context):
    shorts = [n for n in context.neighbors() if n.agent_type == "short"]

    if len(shorts) > 0:
        state.sell_limit *= 1 if state.hold else .9
        state.add_message("market", "sell_limit", {
        "sell_limit": state.sell_limit,
        "shares": state.shares,
      })