import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go # fig.add_hline을 위해 필요

# 데이터 로딩 및 전처리 (이전 답변의 코드와 동일)
def reason():
    df = pd.read_csv('./data/저출산_문제.csv', encoding='utf-8')
    df.rename(columns={'2011': '백분율', '종류별(2)': '종류별'}, inplace=True)
    df = df.query('`구분별(1)` == "서울시"')
    df = df[df['종류별'] != '소계']
    df = df[df['종류별'] != '기타']
    df.drop(columns=['종류별(1)', '구분별(1)', '구분별(2)'], inplace=True)
    df['백분율'] = pd.to_numeric(df['백분율'].astype(str).str.replace(',', '', regex=False), errors='coerce')
    df['종류별'].replace('자녀 양육의 경제적 부담', '경제적부담', inplace=True)

    fig_bar = px.bar(
        df, 
        x='백분율', 
        y='종류별', 
        orientation='h', # 'h'는 horizontal (수평)을 의미합니다. (사실 x, y 위치 변경으로 자동 인식되지만 명시적으로 지정 가능)
        title='출산 포기 요인',
        labels={'백분율': '백분율 (%)', '종류별': '문제 종류'}, # 축 레이블 설정
        color='백분율', # 백분율 값에 따라 막대 색상 변경 (선택 사항)
        # color_continuous_scale=px.colors.sequential.Plasma # 색상 스케일 설정 (선택 사항)
    )

    fig_bar.update_layout(
        yaxis={'categoryorder':'total ascending'} # 백분율이 낮은 것부터 높은 것 순서로 정렬
    )

    st.plotly_chart(fig_bar, use_container_width=True)

def birth_rate():
    df = pd.read_excel('./data/합계출산율.xlsx')
    df.rename(columns={'통계표명:' : '년도'}, inplace=True)
    df = df[df['년도'] != '단위:']
    df = df[df['합계출산율'] !='합계출산율' ]
    df = df.iloc[:55]

    
    fig = px.line(
        df,
        x='년도',
        y='합계출산율',
        title='출산율 변동 추이',
    )

    fig.add_hline(
        y=1.3,                                  # 기준선이 그려질 Y축 값 (초저출산 기준)
        line_color="red",                       # 라인 색상을 빨간색으로 설정
        line_dash="dot",                        # 라인 스타일을 점선으로 설정
        annotation_text="초저출산 기준 (1.3명)", # 라인 옆에 표시될 텍스트
        annotation_position="bottom right"      # 텍스트 위치 설정
    )

    fig.update_traces(mode='lines+markers') # 라인과 마커를 명시적으로 추가

    fig.update_layout(
        xaxis_title='년도',
        yaxis_title='합계출산율',
        hovermode='x unified',
        font=dict(family="Arial", size=12, color="Black"),
        xaxis = dict(
            dtick = "3",
            tickformat = "%Y",
        ),
    )

    st.plotly_chart(fig)

def senior_bar():
    df = pd.read_excel('./data/우리나라_노인인구.xlsx')
    df = df.iloc[:17]

    fig = px.bar(df, x='년도', y='노인인구 비율(%)', title='노인 인구 변화 추이')
    st.plotly_chart(fig)

def senior_pie():

    df = pd.read_excel('./data/연령구분비율.xlsx')

    custom_colors = {
        '청년': 'skyblue',
        '노인': 'red',
        '어린이': 'blue'
    }

    # 4. Plotly Pie Chart 생성
    fig = px.pie(
        df,
        names='인구 구분',
        values='2070년 예상 비율', # 실제 컬럼 이름 사용
        title='2070년 대한민국 인구 연령별 구성비 예측',
        color='인구 구분',
        color_discrete_map={
            # DataFrame의 실제 '인구 구분' 값에 맞게 맵핑
            '어린이': custom_colors['어린이'],
            '청년': custom_colors['청년'],
            '노인 인구': custom_colors['노인'] # 데이터프레임의 실제 값은 '노인 인구'입니다.
        },
        hole=0.4 # 도넛 차트 형태로 변경
    )

    fig.update_traces(
        # 텍스트 레이블을 조각 내부에 표시하고, 레이블과 퍼센트 동시 표시
        textposition='inside',  
        textinfo='percent+label', 
        
        # 도넛 차트 형태로 변경 (0.0에서 1.0 사이 값, 0.5가 일반적)
        hole=0.5, 
        
        pull=[0, 0, 0, 0] 
    )

    fig.update_layout(
        font=dict(family="Arial", size=12),
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.05)
    )

    st.plotly_chart(fig)

def private_tutoring():
    df = pd.read_excel('./data/월급과연도별_사교육비용_추이.xlsx')
    df.fillna(0, inplace=True)
    if df.empty:
        return

    # '월급 분류' 컬럼 외의 연도 컬럼을 확인
    year_columns = [col for col in df.columns if col.isdigit() and 2020 <= int(col) <= 2024]
    
    if not year_columns:
        st.error("연도 컬럼을 찾을 수 없습니다. 컬럼 이름을 확인해 주세요.")
        return

    # --- Wide to Long 변환 ---
    df_long = pd.melt(
        df,
        id_vars=['월급 분류'],
        value_vars=year_columns,
        var_name='년도',
        value_name='금액'
    )
    
    # 4. Plotly Bar Chart에 animation_frame 적용 (핵심)
    fig = px.bar(
        df_long,
        x='월급 분류',
        y='금액',
        color='월급 분류', # 각 막대를 구분하기 위해 색상 적용
        animation_frame='년도',
        animation_group='월급 분류', # 애니메이션 시 막대 구분을 위해 그룹화
        range_y=[0, 70],
        title='사교육 비용 추이 (자녀 1명당)'
    )
    
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 500 # 1초
    
    st.plotly_chart(fig)

def future_population():
    df = pd.read_csv('./data/주요_인구지표_성비_인구성장률_인구구조_부양비_등_전국.csv', encoding='utf-8')
    df.rename(columns={'인구구조,부양비별': '인구구조'}, inplace=True)
    df = df.query('인구구조 == "총인구(명)"')
    df.drop(columns='가정별', inplace=True)
    df = df.T
    df = df.reset_index()
    df.columns = ['년도', '인구수']
    df = df[df['년도'] != '인구구조']

    fig = px.line(
        df, 
        x='년도', 
        y='인구수', 
        title='대한민국 미래 인구 예측 추이',
        labels={'년도': '년도', '인구수': '인구수 (명)'}
    )

    fig.update_traces(mode='lines+markers') # 라인과 마커를 명시적으로 추가

    fig.update_layout(
        hovermode='x unified',
        font=dict(family="Arial", size=12, color="Black"),
        xaxis = dict(
            dtick = "3",
            tickformat = "%Y",
        ),
        yaxis = dict(
            tickformat=",", # 숫자만 쉼표로 표시
            title='인구 수'
        )
    )   

    fig.update_traces(
        # y축 값에 쉼표와 "만 명" 문자열을 추가
        hovertemplate='%{y:,.0f}만 명<extra></extra>' 
    )

    # Y축 레이블은 일반적인 쉼표로 설정하거나 생략합니다.
    st.plotly_chart(fig, use_container_width=True)
