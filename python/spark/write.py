
#write on  CSV
df_pattern_group_parse_result.coalesce(1).write.options(sep ='`').csv(PATTERN_MONIT_CREATION_PATH_CSV, mode='overwrite', header=True)

