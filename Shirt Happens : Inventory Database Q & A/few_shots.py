few_shots = [
    {'Question' : "How many t-shirts do we have left for Makia in extra small size and white color?",
     'SQLQuery' : "SELECT COUNT(*) FROM t_shirts WHERE brand = 'Makia' AND size = 'XS' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer' : '11 t-shirts'},
    {'Question': "How much is the price of the inventory for all large size t-shirts?",
     'SQLQuery':"SELECT SUM(price * stock_quantity) AS total_price FROM t_shirts WHERE size = 'L'",
     'SQLResult': "Result of the SQL query",
     'Answer': 'The total price of the inventory for all large size t-shirts is $342,869.'},
    {'Question': "If we have to sell all the Makia T-shirts today with discounts applied. How much revenue our store will generate (post discounts)?" ,
     'SQLQuery' : "SELECT SUM(t.price * t.stock_quantity * IFNULL((- d.pct_discount / 100), 1)) AS total_revenue FROM t_shirts t LEFT JOIN discounts d ON t.t_shirt_id = d.t_shirt_idWHERE t.brand = 'Makia';",
     'SQLResult': "Result of the SQL query",
     'Answer': 'The total revenue for all Makia brand t-shirts, taking into account any discounts, is $343,582.55.'} ,
     {'Question' : "If i sell all dressman and halti tshirts on discount how much revenue will i have?" ,
      'SQLQuery': "SELECT SUM(t.price * t.stock_quantity * IFNULL((1 - d.pct_discount / 100), 1)) AS total_revenue FROM t_shirts t LEFT JOIN discounts d ON t.t_shirt_id = d.t_shirt_id WHERE t.brand IN ('Dressman', 'Halti');",
      'SQLResult': "Result of the SQL query",
      'Answer' : 'The total revenue for Dressman and Halti brands is 656550.20.'},
    {'Question': "How many yellow color Marimekko t shirts we have available?",
     'SQLQuery' : "SELECT COUNT(*) FROM t_shirts WHERE brand = 'Marimekko' AND color = 'Yellow'",
     'SQLResult': "Result of the SQL query",
     'Answer' : '24'
     }
]