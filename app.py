import streamlit as st
import pandas as pd
import os
from datetime import datetime

# CSVファイルのパス
data_file = 'taxi_data.csv'

# 初期化: データファイルがなければヘッダーを作成
if not os.path.isfile(data_file) or pd.read_csv(data_file).empty:
    df = pd.DataFrame(columns=['日付', '地名', '時間', '金額', '支払い形態'])
    df.to_csv(data_file, index=False)

# 支払い形態と東京23区のリスト
payment_methods = ["現金", "クレジットカード", "電子マネー", "QRコード決済"]
tokyo_districts = [
    "千代田区", "中央区", "港区", "新宿区", "文京区", "台東区", "墨田区", "江東区", "品川区",
    "目黒区", "大田区", "世田谷区", "渋谷区", "中野区", "杉並区", "豊島区", "北区", "荒川区",
    "板橋区", "練馬区", "足立区", "葛飾区", "江戸川区"
]

st.title('営業情報管理システム')

page = st.sidebar.selectbox('ページを選択', ['営業情報の入力', '統計情報'], key='page_select')

if page == '営業情報の入力':
    st.header('営業情報の入力')
    date = st.date_input('日付', key='date_input')
    new_district_toggle = st.checkbox('新しい地名を追加する', key='new_district_toggle')
    if new_district_toggle:
        new_district = st.text_input('新しい地名を追加', key='new_district_input')
    else:
        district_selection = st.selectbox('地名', tokyo_districts, key='district_select')
    time_input = st.text_input('時間 (HH:MM)', key='time_input')
    amount = st.number_input('金額', min_value=0, format='%d', key='amount_input')
    payment_method = st.selectbox('支払い形態', payment_methods, key='payment_method_select')

    try:
        time = datetime.strptime(time_input, '%H:%M')
        valid_time = True
    except ValueError:
        valid_time = False
        if time_input:
            st.error('時間の形式が正しくありません。HH:MM形式で入力してください。', key='time_error')

    if st.button('送信', key='submit_button') and valid_time:
        selected_district = new_district if new_district_toggle else district_selection
        new_data = pd.DataFrame([[date, selected_district, time.strftime("%H:%M"), amount, payment_method]],
                                columns=['日付', '地名', '時間', '金額', '支払い形態'])
        new_data.to_csv(data_file, mode='a', header=False, index=False)
        st.success('記録が正常に追加されました！', key='success_message')

elif page == '統計情報':
    st.header('統計情報')
    df = pd.read_csv(data_file, parse_dates=['日付'])
    df['年'] = df['日付'].dt.year
    df['月'] = df['日付'].dt.month
    df['日'] = df['日付'].dt.day

    option = st.selectbox('集計期間を選択', ['日間', '月間', '年間', '累計'], key='stats_period_select')
