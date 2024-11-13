# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 13:51:07 2024

@author: tmlab
"""


import pandas as pd
from sklearn.metrics import pairwise_distances
import numpy as np
data = pd.read_csv('D:/github/lostark/data/241113_seal_preprocessed.csv')

result = data.groupby(['직업','직업각인','공통각인'])['공통각인 비중'].sum().unstack(fill_value=0)

array = np.array(result)

distance_matrix = pairwise_distances(array, metric='euclidean')
result = result.reset_index()

#%%
result.to_csv('D:/github/lostark/data/contigency_matrix.csv', index = 0)
np.savetxt('D:/github/lostark/data/distance_matrix.csv', distance_matrix, delimiter=',')

#%% 시각화 mds
import matplotlib
matplotlib.use('TkAgg')  # 또는 Qt5Agg
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import seaborn as sns
import numpy as np
from matplotlib import rc
from adjustText import adjust_text  # 겹치는 텍스트 처리 라이브러리

# 한글 폰트 설정
rc('font', family='Malgun Gothic')  # Windows의 경우 'Malgun Gothic', macOS는 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False  # 한글 폰트 설정 시, 마이너스 기호 깨짐 방지

# MDS를 사용하여 2차원으로 축소
mds = TSNE(n_components=2, metric='precomputed', random_state=42, init = "random")
coords = mds.fit_transform(distance_matrix)

# 결과를 데이터프레임으로 변환
df_coords = pd.DataFrame(coords, columns=['Dimension 1', 'Dimension 2'])
df_coords['Group'] = result['직업각인']  # 그룹 레이블 추가
df_coords['Group_color'] = result['직업']  # 그룹 레이블 추가

# 고유한 그룹과 색상 팔레트 설정
groups = df_coords['Group_color'].unique()
palette = sns.color_palette(n_colors=len(groups))
group_colors = dict(zip(groups, palette))

# 산점도 시각화
plt.figure(figsize=(10, 10))
ax = plt.gca()
sns.scatterplot(x='Dimension 1', y='Dimension 2', data=df_coords, hue='Group_color', palette=palette, s=100, ax=ax)
plt.title('MDS Plot of Distance Matrix with Group Labels', fontsize=16)
plt.xlabel('Dimension 1')
plt.ylabel('Dimension 2')
plt.grid(True, linestyle='--', alpha=0.7)  # 격자 추가

# 포인트 위에 그룹 레이블 표시 (adjustText 사용)
texts = []
for i, row in df_coords.iterrows():
    texts.append(plt.text(row['Dimension 1'], row['Dimension 2'], row['Group'],
                          fontsize=10, color='black', weight='bold'))

# 텍스트 위치 자동 조정
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))

plt.legend([], [], frameon=False)  # 범례 제거
plt.tight_layout()
plt.show()