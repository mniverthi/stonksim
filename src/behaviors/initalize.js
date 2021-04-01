/**
 * @param {AgentState} state
 * @param {AgentContext} context
 */
const behavior = (state, context) => {
  const {
    retail_count,
    wsb_count,
    hedge_count,
    melvin_count,
    retail_capital,
    retail_profit,
    retail_sell,
    wsb_capital,
    wsb_profit,
    wsb_sell,
    hedge_short_amount,
    hedge_capital,
    hedge_profit,
    hedge_sell,
    melvin_short_amount,
    melvin_capital,
    melvin_profit,
    melvin_sell,
    steps,
    max_starting_shares
  } = context.globals();

  const market = {
    "agent_name": "market",
    "behaviors": ["@hash/counter/counter.rs", "market.js"],
    "counter": 0,
    "position": [0, 0],
    "sells": [],
  };

  const retail_traders = [...Array(Math.round(retail_count)).keys()].map(i => ({
    "agent_type": "retail",
    "behaviors": ["@hash/counter/counter.rs", "sell.js", "display_trader.js"],
    "position": [i, 3],
    "shares": Math.round(hash_stdlib.stats.uniform.sample(0, max_starting_shares)),
    "counter": 0,
    "capital": retail_capital,
    "profit_threshold": retail_profit,
    "profit_threshold": retail_sell,
  }))

  const wsb_traders = [...Array(Math.round(wsb_count)).keys()].map(i => ({
    "agent_type": "wsb",
    "behaviors": ["@hash/counter/counter.rs", "sell.js", "display_trader.js"],
    "position": [i, 4],
    "shares": Math.round(hash_stdlib.stats.uniform.sample(0, max_starting_shares)),
    "counter": 0,
    "capital": wsb_capital,
    "profit_threshold": wsb_profit,
    "profit_threshold": wsb_sell,
  }))

  const total_shares = hash_stdlib.stats.sum(retail_traders.map(t => t.shares))
      + hash_stdlib.stats.sum(wsb_traders.map(t => t.shares))

  const hedge_funds = [...Array(hedge_count).keys()].map(i => ({
    "agent_type": "hedge",
    "behaviors": ["@hash/counter/counter.rs", "cover_short.js"],
    "position": [i, 5],
    "shorts": hedge_short_amount,
    "counter": 0,
    "price": 1,
    "cost": 0,
    "capital": hedge_capital,
    "profit_threshold": hedge_profit,
    "profit_threshold": hedge_sell,
  }))

  const melvin_funds = [...Array(melvin_count).keys()].map(i => ({
    "agent_type": "melvin",
    "behaviors": ["@hash/counter/counter.rs", "cover_short.js"],
    "position": [i, 6],
    "shorts": melvin_short_amount,
    "counter": 0,
    "price": 1,
    "cost": 0,
    "capital": melvin_capital,
    "profit_threshold": melvin_profit,
    "profit_threshold": melvin_sell,
  }))


  const agents = [...retail_traders, ...wsb_traders, ...hedge_funds, ...melvin_funds, market];
  agents.forEach(a => state.addMessage("hash", "create_agent", a));

  state.addMessage("hash", "remove_agent");
};
