SELECT SUM(amount)                                 AS tot_amt
     ,   SUM(CASE WHEN amount >=  0 THEN amount END/*else is null*/)  AS pos_amt
     ,   SUM(CASE WHEN amount <   0 THEN amount END)  AS neg_amt
FROM some_table;

//else
select CASE WHEN category LIKE 'ao%'      THEN 'ao'
            WHEN category LIKE 'a1%'      THEN 'a1'
                                          ELSE LOWER(category)
       END
from some_table