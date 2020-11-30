import pyspark.sql.functions as F


df_repr_msg_by_sdr_group = df_inputs\
    .groupby('sdr')\
    .agg(F.first('msg').alias('selected_msg'))