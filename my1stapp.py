import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.title('シンプルなMarketing Automationツール')

# ユーザーデータの作成
@st.cache_data
def create_user_data():
    data = {
        'ユーザーID': range(1, 101),
        '最終アクセス日': [datetime.now() - timedelta(days=i) for i in range(100)],
        'メール開封回数': [i % 10 for i in range(100)],
        'ウェブサイト訪問回数': [i % 15 for i in range(100)]
    }
    return pd.DataFrame(data)

user_data = create_user_data()

# セグメンテーション機能
st.header('ユーザーセグメンテーション')
days_inactive = st.slider('何日以上アクセスのないユーザーを抽出しますか？', 0, 30, 7)
inactive_users = user_data[user_data['最終アクセス日'] < datetime.now() - timedelta(days=days_inactive)]
st.write(f'{days_inactive}日以上アクセスのないユーザー数: {len(inactive_users)}')

# エンゲージメントスコア計算
def calculate_engagement_score(row):
    return row['メール開封回数'] * 2 + row['ウェブサイト訪問回数']

user_data['エンゲージメントスコア'] = user_data.apply(calculate_engagement_score, axis=1)

# エンゲージメント分析
st.header('ユーザーエンゲージメント分析')
fig = go.Figure(data=[go.Scatter(x=user_data['ユーザーID'], y=user_data['エンゲージメントスコア'], mode='markers')])
fig.update_layout(title='ユーザーごとのエンゲージメントスコア', xaxis_title='ユーザーID', yaxis_title='エンゲージメントスコア')
st.plotly_chart(fig)

# 自動メール配信シミュレーション
st.header('自動メール配信シミュレーション')
engagement_threshold = st.slider('エンゲージメントスコアのしきい値を設定', 0, 50, 25)
users_to_email = user_data[user_data['エンゲージメントスコア'] < engagement_threshold]
st.write(f'メール配信対象ユーザー数: {len(users_to_email)}')
if st.button('メール配信をシミュレート'):
    st.success(f'{len(users_to_email)}人のユーザーにメールを配信しました。')

# ユーザーデータの表示
st.header('ユーザーデータ')
st.dataframe(user_data)
