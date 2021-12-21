
df_inputs.join(df2, how='left', on=['a'])
df_inputs.join(df2, (df_inputs.a == df2.a) & df_inputs.b == df2.b)

df_inputs.alias("a").join(df2.alias("b"), (col("a.a") == col("b.a") & col("a.b") == col("b.b"))\
    .select(list(map(lambda c: f"a.{c}", df_inputs.columns)) + ["b_column"])