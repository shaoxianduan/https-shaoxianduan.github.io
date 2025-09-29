import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ------------------ Page Config ------------------
st.set_page_config(page_title="SOX vs DJIA", layout="wide")
st.title("📈 SOX vs DJIA Positive/Negative Return Comparison")

# ------------------ Dynamic Dates ------------------
end_date = datetime.today()
start_date = end_date - timedelta(days=3*365)  # Last 3 years
start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")

# ------------------ Download Data ------------------
sox = yf.download("^SOX", start=start_str, end=end_str, auto_adjust=False)
djia = yf.download("^DJI", start=start_str, end=end_str, auto_adjust=False)

# ------------------ Calculate Daily Returns and Cumulative Returns ------------------
for df in [sox, djia]:
    df['Return'] = df['Adj Close'].pct_change()
    df['Cumulative_Return'] = (1 + df['Return']).cumprod()

# ------------------ Define Time Windows ------------------
end_dt = sox.index[-1]
window_dict = {
    "Last 1 Month": 21,
    "Last 3 Months": 63,
    "Last 6 Months": 126,
    "Year to Date": (end_dt - datetime(end_dt.year, 1, 1)).days,
    "Last 1 Year": 252,
    "Last 3 Years": len(sox)
}

# ------------------ Frontend Time Window Selection ------------------
selected_window = st.radio("Select Time Window", list(window_dict.keys()))
period_days = window_dict[selected_window]
period_days = max(2, min(period_days, len(sox)))  # Ensure safe range

sox_window = sox.iloc[-period_days:]
djia_window = djia.iloc[-period_days:]

# ------------------ Display Total Returns ------------------
returns_dict = {}
for label, df_window in zip(['SOX', 'DJIA'], [sox_window, djia_window]):
    try:
        start_price = float(df_window['Adj Close'].iloc[0])
        end_price = float(df_window['Adj Close'].iloc[-1])
        returns_dict[label] = (end_price / start_price - 1) * 100
    except:
        returns_dict[label] = float('nan')

st.subheader(f"{selected_window} Total Return (%)")
st.table(pd.DataFrame.from_dict(returns_dict, orient='index',
         columns=['Total Return (%)']).round(2))

# ------------------ Align Window Lengths ------------------
min_len = min(len(sox_window), len(djia_window))
sox_window = sox_window.iloc[-min_len:]
djia_window = djia_window.iloc[-min_len:]

# ------------------ Normalize Cumulative Returns ------------------
sox_norm = sox_window['Adj Close'].astype(
    float).squeeze() / float(sox_window['Adj Close'].iloc[0]) * 100
djia_norm = djia_window['Adj Close'].astype(
    float).squeeze() / float(djia_window['Adj Close'].iloc[0]) * 100
dates = sox_window.index

# ------------------ Difference ------------------
diff = sox_norm - djia_norm  # 1D Series

# ------------------ Display Final Difference ------------------
final_diff = diff.iloc[-1]  # scalar value
st.metric(label="Final Difference (SOX - DJIA, % points)",
          value=f"{final_diff:.2f}")

# ------------------ Plot Normalized Cumulative Returns + Difference ------------------
st.subheader("Normalized Cumulative Returns (Start = 100) + Difference")
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(dates, sox_norm, label='SOX', color='blue')
ax1.plot(dates, djia_norm, label='DJIA', color='orange')
ax1.set_xlabel("Date")
ax1.set_ylabel("Normalized Price (Start = 100)")
ax1.legend(loc="upper left")
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(dates, diff, label="SOX - DJIA (Difference)",
         color="green", linestyle="--")
ax2.set_ylabel("Difference (SOX - DJIA)")
ax2.legend(loc="upper right")
ax1.set_title(f"SOX vs DJIA Comparison & Difference ({selected_window})")
st.pyplot(fig)

# ------------------ Plot Cumulative Difference ------------------
st.subheader("Cumulative Difference Over Time (SOX - DJIA)")
diff_filled = diff.fillna(0).astype(float)
cumulative_diff = diff_filled.cumsum()

fig2, ax = plt.subplots(figsize=(12, 4))
ax.fill_between(dates, cumulative_diff.values, color='green', alpha=0.3)
ax.plot(dates, cumulative_diff.values,
        color='green', label="Cumulative Difference")
ax.set_xlabel("Date")
ax.set_ylabel("Cumulative Difference (% points)")
ax.grid(True)
ax.legend()
st.pyplot(fig2)
