select *,case when unit = "Billions" then revenue*1000
when unit = "Thousand" then revenue/1000 else revenue end - case when unit = "Billions" then budget*1000
when unit = "Thousand" then budget/1000 else budget end as profit_millions,(revenue-budget)*100/budget profit_pct from financials;

