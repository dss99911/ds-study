
#add column
df_matched.withColumn('pattern_group_num',F.lit(iter_num))

#remove column
df_others.drop('selected_msg')