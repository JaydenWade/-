import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import akshare as ak

# 获取品种代码
# futures_display_main_sina_df = ak.futures_display_main_sina()
futures_display_main_sina_df = ["V0","P0","M0","JD0","Y0","C0","A0","MA0","FG0","SF0","FU0","RB0","SA0","SP0","PB0","IC0","IF0"]
# 获取价格

futures_main_sina_hist = ak.futures_main_sina(symbol="CJ0", start_date="20230612", end_date="20240812")

# 计算指数移动平均线（EMA）
ema_short_period = 5
ema_long_period = 20

ema_short = pd.Series(futures_main_sina_hist["收盘价"]).ewm(span=ema_short_period, adjust=False).mean()
ema_long = pd.Series(futures_main_sina_hist["收盘价"]).ewm(span=ema_long_period, adjust=False).mean()

# 确定金叉和死叉信号
signals = np.where(ema_short > ema_long, 1, -1)
positions = pd.Series(signals).diff()
    

# 可视化价格和移动平均线
plt.figure(figsize=(10, 6))
plt.plot(futures_main_sina_hist["收盘价"], label='Price')
plt.plot(ema_short, label=f'EMA {ema_short_period}')
plt.plot(ema_long, label=f'EMA {ema_long_period}')
plt.title('Price with EMAs and Signal')
plt.xlabel('Time')
plt.ylabel('Price')

golden_cross_indices = positions.index[positions == 2]
death_cross_indices = positions.index[positions == -2]

for index in golden_cross_indices:
    plt.scatter(index, futures_main_sina_hist["收盘价"][index], color='g', marker='o', s=50, label='')
    plt.text(index, futures_main_sina_hist["收盘价"][index], str(futures_main_sina_hist["收盘价"][index]))  # 添加显示 y 轴数值

for index in death_cross_indices:
    plt.scatter(index, futures_main_sina_hist["收盘价"][index], color='r', marker='o', s=50, label='')
    plt.text(index, futures_main_sina_hist["收盘价"][index], str(futures_main_sina_hist["收盘价"][index]))  # 添加显示 y 轴数值

plt.legend()
plt.show()