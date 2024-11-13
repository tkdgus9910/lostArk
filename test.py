# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 04:16:02 2024

@author: tmlab
"""


import streamlit as st
import pandas as pd
import plotly.express as px
import os
import matplotlib
matplotlib.use("Agg")

import matplotlib.font_manager as fm

import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import seaborn as sns
import numpy as np
from matplotlib import rc
from adjustText import adjust_text  # 겹치는 텍스트 처리 라이브러리
import requests

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_directory)

#%%

from matplotlib import font_manager

# Specify the path to your font files
font_dirs = ['./fonts/']  # Replace with your font directory
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    font_manager.fontManager.addfont(font_file)
font_family = font_manager.FontProperties(fname=font_files[0]).get_name()
plt.rcParams['font.family'] = font_family


#%%

# Load data
df = pd.read_csv('./data/241113_seal_preprocessed.csv')
contigency_mat_df= pd.read_csv('./data/contigency_matrix.csv')

# Load the array
distance_matrix = np.loadtxt('./data/distance_matrix.csv', delimiter=',')

st.title('유효각인 대시보드')

# Sidebar for page selection
page = st.sidebar.radio("페이지를 선택하시오:", ["직업별 유효 공통각인", "공통각인별 유효 직업각인", "직업각인 맵"])


if page == "직업별 유효 공통각인":
    st.header("직업별 각인 보기")
    
    # Sidebar for job selection
    job = st.sidebar.selectbox('직업을 선택하시오:', df['직업'].unique())
    
    # Filter available engravings based on the selected job
    available_engravings = df[df['직업'] == job]['직업각인'].unique()
    
    # Sidebar for engraving selection
    engraving = st.sidebar.selectbox('직업각인을 선택하시오:', available_engravings)
    
    # Filter data based on job and engraving selection
    filtered_df = df[(df['직업'] == job) & (df['직업각인'] == engraving)]
    
    # Display filtered data
    # st.dataframe(filtered_df)
    
    # 바 차트 생성
    fig = px.bar(
        filtered_df,
        x="공통각인",
        y="공통각인 비중",
        color="공통각인_구분",
        title="Bar Chart with Categories and Legend",
        barmode="group",
        template="plotly_white"
    )
    
    # Update layout for better visibility, spacing, and size
    fig.update_layout(
        title=dict(font=dict(size=24)),  # Title font size
        xaxis=dict(
            title=dict(font=dict(size=18)),  # X-axis label font size
            tickfont=dict(size=14),  # X-axis tick font size
            tickangle=-45,  # Rotate tick labels for better fit
            tickmode="linear"  # Show all X-axis values
        ),
        yaxis=dict(title=dict(font=dict(size=18)), tickfont=dict(size=14)),  # Y-axis settings
        legend=dict(font=dict(size=16)),  # Legend font size
        bargap=0.4,  # Adjust bar spacing for wider gaps
        width=1200,  # Set the width of the figure
        height=600  # Set the height of the figure
    )
    
    # Manually adjust X-axis tick spacing and widen categories
    fig.update_xaxes(
        categoryorder="array",  # Ensure order of categories
        ticklabelposition="outside"  # Move labels outside for clarity
    )


    
    # Streamlit에서 차트 표시
    st.plotly_chart(fig)


elif page == "공통각인별 유효 직업각인":
    st.header("공통각인별 유효직업 보기")
    
    # Common engraving selection
    common_engraving = st.selectbox('공통각인을 선택하시오:', df['공통각인'].unique())
    
    # Filter jobs based on selected common engraving
    filtered_df = df[(df['공통각인'] == common_engraving)]
    
    # 바 차트 생성
    fig = px.bar(
        filtered_df,
        x="직업각인",
        y="공통각인 비중",
        color="공통각인_구분",
        title="Bar Chart with Categories and Legend",
        barmode="group",
        template="plotly_white"
    )
    
    # Update layout for better visibility, spacing, and size
    fig.update_layout(
        title=dict(font=dict(size=24)),  # Title font size
        xaxis=dict(
            title=dict(font=dict(size=18)),  # X-axis label font size
            tickfont=dict(size=14),  # X-axis tick font size
            tickangle=-45,  # Rotate tick labels for better fit
            tickmode="linear"  # Show all X-axis values
        ),
        yaxis=dict(title=dict(font=dict(size=18)), tickfont=dict(size=14)),  # Y-axis settings
        legend=dict(font=dict(size=16)),  # Legend font size
        bargap=0.4,  # Adjust bar spacing for wider gaps
        width=1200,  # Set the width of the figure
        height=600  # Set the height of the figure
    )
    
    # Manually adjust X-axis tick spacing and widen categories
    fig.update_xaxes(
        categoryorder="array",  # Ensure order of categories
        ticklabelposition="outside"  # Move labels outside for clarity
    )


    
    # Streamlit에서 차트 표시
    st.plotly_chart(fig)

elif page == "직업각인 맵":

    # MDS를 사용하여 2차원으로 축소
    mds = TSNE(n_components=2, metric='precomputed', random_state=42, init = "random")
    coords = mds.fit_transform(distance_matrix)

    # 결과를 데이터프레임으로 변환
    df_coords = pd.DataFrame(coords, columns=['Dimension 1', 'Dimension 2'])
    df_coords['Group'] = contigency_mat_df['직업각인']  # 그룹 레이블 추가
    df_coords['Group_color'] = contigency_mat_df['직업']  # 그룹 레이블 추가

    # 고유한 그룹과 색상 팔레트 설정
    groups = df_coords['Group_color'].unique()
    palette = sns.color_palette(n_colors=len(groups))
    group_colors = dict(zip(groups, palette))

        
    # 산점도 시각화
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.scatterplot(
        x='Dimension 1', y='Dimension 2', data=df_coords,
        hue='Group_color', palette=palette, s=100, ax=ax
    )
    ax.set_title('MDS Plot of Distance Matrix with Group Labels', fontsize=16)
    ax.set_xlabel('Dimension 1')
    ax.set_ylabel('Dimension 2')
    ax.grid(True, linestyle='--', alpha=0.7)  # 격자 추가
    
    # 포인트 위에 그룹 레이블 표시 (adjustText 사용)
    texts = []
    for i, row in df_coords.iterrows():
        texts.append(
            ax.text(
                row['Dimension 1'], row['Dimension 2'], row['Group'],
                fontsize=10, color='black', weight='bold'
            )
        )
    
    # 텍스트 위치 자동 조정
    adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))
    
    ax.legend([], [], frameon=False)  # 범례 제거
    plt.tight_layout()
    
    # Streamlit을 사용하여 그래프 표시
    st.pyplot(fig)

# pip list --format=freeze > requirements.txt
