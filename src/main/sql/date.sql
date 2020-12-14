
//get -180 day from the date
select DATE_ADD('DAY', -180, CAST(FROM_UNIXTIME(report_file_time/1000) AS DATE)) from dates
select  DATE_DIFF('MONTH', report_dt, CAST(transaction_date AS DATE)) from dates