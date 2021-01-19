-- mart.abc
-- automation http://jason-heo.github.io/programming/2017/02/17/parquet-to-hive-table.html
CREATE EXTERNAL TABLE mart.cumulative_point_status(
                                                      user_id string,
                                                      user_status string,
                                                      amount decimal(12,2)
)
    PARTITIONED BY (key STRING)
    STORED AS PARQUET
    LOCATION 's3://hyun/analysis/mart/abc';