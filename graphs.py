import pandas as pd
import streamlit as st
import plotly.express as px

def set_first_row_as_header(df) :  # 레코드를 컬럼으로 변경
    df.columns = df.iloc[0]  # 0번째 행을 데이터프레임의 column으로 설정
    df = df[1 : ]  # 데이터프레임을 1번째 행부터 보여줌

    return df

def rename_df_columns(df) :  # 컬럼명 변경
    df.rename(
        columns = {
            '특성별(1)' : '분류',
            '특성별(2)' : '하위분류',
            '2024' : '있다',
            '2024.1' : '없다'
        },
        level = 0,
        inplace = True
    )
    if (df.columns.nlevels) > 1 :  # df.columns.nlevels는 1부터 시작
        df.rename(
            columns = {
                '특성별(1)' : '분류',
                '특성별(2)' : '하위분류',
            },
            level = 1,
            inplace = True
        )

    return df

def convert_to_numeric(df, col) :
    df[col] = pd.to_numeric(df[col], errors = 'coerce') # 'coerce' : 결측값을 NaN 으로 강제 변환
    df[col] = df[col].fillna(0)
    
    return df


def check_marriage_intention() :  # 향후 자녀 출산 의향
    df = pd.read_csv('./data/향후_결혼_계획_20251108162558.csv', encoding = 'utf-8')

    st.header("향후 결혼 계획")

    # .pipe(함수명, 추가 인수) : 이전 단계의 df를 함수의 첫 번째 인수로 전달, 나머지 인수를 순서대로 전달
    df = (
        set_first_row_as_header(df)
        .pipe(rename_df_columns)
        .pipe(convert_to_numeric, '있다 (%)')
        .pipe(convert_to_numeric, '없다 (%)')
    )

    unique_group = df['분류'].unique().tolist()
    category_selectbox = st.selectbox(
        '분류',
        unique_group,
        key = 'check_marriage_intention_selectbox'
    )

    df = df.query('분류 == @category_selectbox')
    df_melt = pd.melt(
        df,
        id_vars = ['분류', '하위분류'],  # 고정 열
        var_name = '결혼의향',  
        value_name = '백분율(%)'
    )

    chart = px.bar(
        data_frame = df_melt,
        x = '결혼의향',
        y = '백분율(%)',
        color = '하위분류', 
        barmode = 'group', 
        range_y = [20, 70],
        title = '결혼 의향 백분율'
    )

    st.plotly_chart(chart, key = 'check_marriage_intention_chart')
    st.dataframe(df, hide_index = True)

def Intention_to_have_children_in_the_future() :  # 향후 자녀 출산 의향
    df = pd.read_csv('./data/향후_자녀_출산_의향_20251108162649.csv', encoding = 'utf-8')

    st.header("향후 자녀 출산 의향")

    # .pipe(함수명, 추가 인수) : 이전 단계의 df를 함수의 첫 번째 인수로 전달, 나머지 인수를 순서대로 전달
    df = (
        set_first_row_as_header(df)
        .pipe(rename_df_columns)
        .pipe(convert_to_numeric, '있다 (%)')
        .pipe(convert_to_numeric, '없다 (%)')
    )

    unique_group = df['분류'].unique().tolist()
    category_selectbox = st.selectbox(
        '분류',
        unique_group,
        key = 'Intention_to_have_children_in_the_future_selectbox'
    )

    df = df.query('분류 == @category_selectbox')
    df_melt = pd.melt(
        df,
        id_vars = ['분류', '하위분류'],  # 고정 열
        var_name = '자녀출산의향',  
        value_name = '백분율(%)'
    )

    chart = px.bar(
        data_frame = df_melt,
        x = '자녀출산의향',
        y = '백분율(%)',
        color = '하위분류', 
        barmode = 'group', 
        range_y = [20, 70],
        title = '결혼 의향 백분율'
    )

    st.plotly_chart(chart, key = 'Intention_to_have_children_in_the_future_chart')
    st.dataframe(df, hide_index = True)


def Attitudes_toward_Children_and_Child_Rearing() :
    df = pd.read_csv('./data/자녀와_자녀_양육에_대한_생각.csv', encoding = 'utf-8', header = [1, 2])

    st.subheader('자녀와 자녀 양육에 대한 생각')

    # .pipe(함수명, 추가 인수) : 이전 단계의 df를 함수의 첫 번째 인수로 전달, 나머지 인수를 순서대로 전달
    df = rename_df_columns(df)

    unique_column_group = df.columns.get_level_values(0).unique().tolist()[2 : ]  # '분류'와 '하위분류'도 list에 들어가기 때문에 슬라이싱
    topic_selectbox = st.selectbox(
        'topic',
        unique_column_group,
        key = 'Attitudes_toward_Children_and_Child_Rearing_selectbox_topic'
    )

    df = df[['분류', '하위분류', topic_selectbox]]

    df.columns = df.columns.droplevel(0)  # level0은 위에서 다 처리했으므로 drop(굳이 MultiIndex로 둘 필요 없음)

    df = convert_to_numeric(df, '전혀 그렇지 않다 (%)')

    unique_group_category = df['분류'].unique().tolist()
    category_selectbox = st.selectbox(
        '분류',
        unique_group_category,
        key = 'check_marriage_intention_selectbox_category'
    )

    df = df.query('분류 == @category_selectbox')


    unique_group_subCategory = df['하위분류'].unique().tolist()
    if category_selectbox != '전체' : 
        subCategory_radio = st.radio(
            '하위분류',
            unique_group_subCategory,
            key = 'check_marriage_intention_selectbox_subCategory'
        )

        df = df.query('하위분류 == @subCategory_radio')
    else : 
        subCategory_radio = '전체'

    df_melt = pd.melt(
        df,
        id_vars = ['분류', '하위분류'],
        var_name = 'scale',
        value_name = '백분율(%)'
    )

    pie_chart = px.pie(
        data_frame = df_melt, 
        names = 'scale', 
        values = '백분율(%)', 
        title = '[전체] 백분율' if (subCategory_radio == '전체') else ('[' + category_selectbox + ']에 따른 [' + subCategory_radio + '] 백분율'),
        hole = 0.3 
    )

    st.plotly_chart(pie_chart)

def home() :
    check_marriage_intention()
    Intention_to_have_children_in_the_future()
    Attitudes_toward_Children_and_Child_Rearing()