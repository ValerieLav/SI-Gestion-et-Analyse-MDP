##########################################
#                                        #
#     Mélange du Fichier RockYou.txt     #
#                                        #
##########################################

import pandas as pd

pathfile = r'rockyou.txt'
df_no_suffle = pd.read_csv(pathfile,
                           on_bad_lines='skip',
                           encoding="latin-1",
                           header=None,
                           names=["pwd"])
suffled_df = df_no_suffle.sample(frac=1).reset_index(drop=True)
suffled_df.to_csv(f'rockyou.txt')

# Test
print(suffled_df.iloc[0])