import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import akshare as ak
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

# 邮件发送相关设置
sender_email = "593849745@qq.com"
sender_password = "lxlvlpygvlxsbajb"
receiver_email = "593849745@qq.com"

def send_email_qq(subject, body):
    # 创建一个带附件的邮件实例
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # 邮件正文
    message.attach(MIMEText(body, "plain"))

    # 创建 SMTP 会话
    with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# 获取当前日期
today = datetime.date.today()
start_date = (today - datetime.timedelta(days=60)).strftime("%Y%m%d")
end_date = today.strftime("%Y%m%d")

# 获取品种代码
futures_display_main_sina_df = ak.futures_display_main_sina()

# 用于存储每个品种的金叉死叉信号结果
signal_results = {}

for symbol in futures_display_main_sina_df["symbol"]:
    futures_main_sina_hist = ak.futures_main_sina(symbol=symbol, start_date=start_date, end_date=end_date)

    # 计算指数移动平均线（EMA）
    ema_short_period = 5
    ema_long_period = 20

    ema_short = pd.Series(futures_main_sina_hist["收盘价"]).ewm(span=ema_short_period, adjust=False).mean()
    ema_long = pd.Series(futures_main_sina_hist["收盘价"]).ewm(span=ema_long_period, adjust=False).mean()

    # 确定金叉和死叉信号
    signals = np.where(ema_short > ema_long, 1, -1)
    positions = pd.Series(signals).diff()

    # 获取最新日期的信号
    latest_signal = positions.iloc[-1] if len(positions) > 0 else 0

    if latest_signal == 2:
        signal_results[symbol] = "金叉信号"
    elif latest_signal == -2:
        signal_results[symbol] = "死叉信号"
    else:
        signal_results[symbol] = "无交易信号"

# 构建邮件内容
mail_body = ""
for symbol, signal in signal_results.items():
    if signal!= "无交易信号":
        mail_body += f"{symbol}: {signal}\n"

if mail_body:
    subject = "期货交易信号提醒"
    send_email_qq(subject, mail_body)
else:
    subject = "无期货交易信号"
    send_email_qq(subject, "当前没有出现交易信号的品种。")