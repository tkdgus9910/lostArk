# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 04:16:02 2024

@author: tmlab
"""



#%%
import streamlit as st
import pandas as pd
import plotly.express as px

# Load sample data
df = pd.read_csv('D:/github/lostark/241113_seal_preprocessed.csv')

st.title('직업각인 별 주요 공통각인 목록')

# Sidebar for page selection
page = st.sidebar.radio("페이지를 선택하시오:", ["직업별 각인", "공통각인별 유효직업"])


if page == "직업별 각인":
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
    
    # Streamlit에서 차트 표시
    st.plotly_chart(fig)


elif page == "공통각인별 유효직업":
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
    
    # Streamlit에서 차트 표시
    st.plotly_chart(fig)


