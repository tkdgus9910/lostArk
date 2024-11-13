#%% PLOTTING

import pandas as pd

result_df = pd.read_csv('D:/github/lostark/241113_seal.csv')

# 90이상 필수각인
# 30-90 주요각인
# 선필-30 서브각인
# 선필미만 제외

def seal_classify(value, x) :
    if value >= 90 :
        return('필수각인')
    elif value >= 30 : 
        return('주요각인')
    elif value > x:
        return('보조각인')
    else : 
        return('제외')

result_df_ = pd.DataFrame()

for job in set(result_df['직업각인']) :
    temp_df = result_df.loc[result_df['직업각인'] == job, : ].reset_index(drop = 1)
    sp_idx = temp_df.loc[temp_df['공통각인'] == '선수필승','공통각인 비중'].reset_index(drop = 1)[0]
    temp_df['공통각인_구분'] = temp_df['공통각인 비중'].apply(lambda x : seal_classify(x, sp_idx))
    
    result_df_ = pd.concat([result_df_, temp_df], axis= 0 )
    

result_df_ = result_df_.loc[result_df_['공통각인_구분'] != '제외',:].reset_index(drop = 1)

result_df_.to_csv('D:/github/lostark/241113_seal_preprocessed.csv', index = 0)