select CAST(transaction_date AS DATE),//string to date
       CAST(FROM_UNIXTIME(report_file_time/1000) AS DATE) // milli second to date
from data