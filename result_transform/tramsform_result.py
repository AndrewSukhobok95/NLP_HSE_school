import pandas as pd

def entities_sum(ent_list):
    df = pd.DataFrame(ent_list)
    df = df.groupby([0, 1])[2].sum().reset_index()
    return df.values.tolist()

# IF THE INPUT IS 

# ent_list = [
#     ['a', 'b', 1],
#     ['c', 'b', 2],
#     ['a', 'b', 3],
#     ['b', 'c', 4],
#     ['b', 'c', -4]
#        ]

# THEN RESULT OF

# entities_sum(ent_list)

# IS

# [
# 	['a', 'b', 4],
# 	['b', 'c', 0],
# 	['c', 'b', 2]
# ]
