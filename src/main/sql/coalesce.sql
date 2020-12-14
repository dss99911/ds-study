//find first not null value.

get 0 if null
SELECT  some_thing,
        SUM(    COALESCE(bank_account_credited_amount,  0)
            +   COALESCE(card_credited_amount,          0)
            +   COALESCE(credit_card_credited_amount,   0)
            +   COALESCE(debit_card_credited_amount,    0)
            +   COALESCE(wallet_credited_amount,        0)
            +   COALESCE(upi_credited_amount,           0)
            +   COALESCE(cash_credited_amount,          0)
            +   COALESCE(unknown_credited_amount,       0)
            )
FROM SOME_TABLE