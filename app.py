import streamlit as st
import pandas as pd
from datetime import datetime

# CSVファイルのパス
data_file = 'taxi_data.csv'

# 初期化: データファイルがなければヘッダーを作成
if not os.path.isfile(data_file) or pd.read_csv(data_file).empty:
    df = pd.DataFrame(columns=['日付', '地名', '時間', '金額', '支払い形態'])
    df.to_csv(data_file, index=False)
else:
    # データの読み込みと確認
    df = pd.read_csv(data_file, parse_dates=['日付'])
    print("データフレームの先頭5行:", df.head())
    print("日付列のデータ型:", df['日付'].dtype)

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
    # 営業情報入力のコードはここに続く（省略）

elif page == '統計情報':
    st.header('統計情報')
    if df.empty:
        st.write("データがありません。")
    else:
        df['時'] = df['日付'].dt.hour
        option = st.selectbox('集計期間を選択', ['日間', '月間', '年間', '累計'], key='stats_period_select')
        
        if option == '日間':
            selected_day = st.date_input("日付を選択")
            filtered_data = df[df['日付'] == pd.Timestamp(selected_day)]
            if not filtered_data.empty:
                sorted_data = filtered_data.sort_values('金額', ascending=False)
                st.dataframe(sorted_data[['日付', '地名', '金額', '支払い形態']])
            else:
                st.write("選択された日にデータはありません。")
        
        elif option == '月間':
            selected_month = st.selectbox('月を選択', range(1, 13), key='month_select')
            selected_year = st.selectbox('年を選択', df['日付'].dt.year.unique(), key='year_select')
            filtered_data = df[(df['日付'].dt.year == selected_year) & (df['日付'].dt.month == selected_month)]
            if not filtered_data.empty:
                sorted_data = filtered_data.sort_values('金額', ascending=False)
                st.dataframe(sorted_data[['日付', '地名', '金額', '支払い形態']])
            else:
                st.write("選択された月にデータはありません。")
        
        elif option == '年間':
            selected_year = st.selectbox('年を選択', df['日付'].dt.year.unique(), key='year_select_annual')
            filtered_data = df[df['日付'].dt.year == selected_year]
            if not filtered_data.empty:
                sorted_data = filtered_data.sort_values('金額', ascending=False)
                st.dataframe(sorted_data[['日付', '地名', '金額', '支払い形態']])
            else:
                st.write("選択された年にデータはありません。")
        
        elif option == '累計':
            sorted_data = df.sort_values('金額', ascending=False)
            st.dataframe(sorted_data[['日付', '地名', '金額', '支払い形態']])
