import streamlit as st
import pandas as pd
import os
from datetime import datetime

# CSVファイルのパス
data_file = 'taxi_data.csv'

# 初期化: データファイルがなければヘッダーを作成
if not os.path.isfile(data_file):
    df = pd.DataFrame(columns=['日付', '23区', '時間', '金額', '支払い形態'])
    df.to_csv(data_file, index=False)

# 支払い形態と東京23区のリスト
payment_methods = ["現金", "クレジットカード", "電子マネー", "QRコード決済","GoPAY"]
tokyo_districts = ["千代田区", "中央区", "港区", "新宿区", "文京区", ...]

st.title('営業統計管理システム')

# ページの選択
page = st.sidebar.selectbox('ページを選択', ['データ入力', '統計情報'])

if page == 'データ入力':
    st.header('営業情報の入力')
    date = st.date_input('日付')
    address = st.selectbox('23区', tokyo_districts)
    time_input = st.text_input('時間 (HH:MM)')
    amount = st.number_input('金額', min_value=0, format='%d')
    payment_method = st.selectbox('支払い形態', payment_methods)

    try:
        time = datetime.strptime(time_input, '%H:%M')
        valid_time = True
    except ValueError:
        valid_time = False
        if time_input:
            st.error('時間の形式が正しくありません。HH:MM形式で入力してください。')

    if st.button('送信') and valid_time:
        new_data = pd.DataFrame([[date, address, time.strftime("%H:%M"), amount, payment_method]],
                                columns=['日付', '23区', '時間', '金額', '支払い形態'])
        new_data.to_csv(data_file, mode='a', header=False, index=False)
        st.success('記録が正常に追加されました！')

elif page == '統計情報':
    st.header('統計情報')
    df = pd.read_csv(data_file, parse_dates=['日付'])
    df['年'] = df['日付'].dt.year
    df['月'] = df['日付'].dt.month
    df['日'] = df['日付'].dt.day

    # 日間、月間、年間、累計の集計
    option = st.selectbox('集計期間を選択', ['日間', '月間', '年間', '累計'])
    if option == '日間':
        selected_date = st.date_input("日付を選択")
        filtered_data = df[df['日付'] == pd.Timestamp(selected_date)]
        summary = filtered_data.groupby('23区')['金額'].sum()
    elif option == '月間':
        year_month = st.selectbox('年月を選択', pd.unique(df['年'].astype(str) + '-' + df['月'].astype(str)))
        year, month = map(int, year_month.split('-'))
        filtered_data = df[(df['年'] == year) & (df['月'] == month)]
        summary = filtered_data.groupby('23区')['金額'].sum()
    elif option == '年間':
        selected_year = st.selectbox('年を選択', pd.unique(df['年']))
        filtered_data = df[df['年'] == selected_year]
        summary = filtered_data.groupby('23区')['金額'].sum()
    elif option == '累計':
        summary = df.groupby('23区')['金額'].sum()

    st.subheader(f'{option}の集計')
    st.bar_chart(summary)
