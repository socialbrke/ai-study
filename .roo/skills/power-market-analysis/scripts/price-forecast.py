#!/usr/bin/env python3
# 电力市场价格预测脚本
# 输入: market-data.csv (使用references/market-template.csv格式)
# 输出: 未来3小时价格预测和交易建议

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import sys

def main():
    # 读取市场数据
    try:
        df = pd.read_csv('market-data.csv')
        print(f"成功读取 {len(df)} 条市场数据记录")
    except FileNotFoundError:
        print("错误: 未找到market-data.csv文件，请确保数据文件存在")
        print("请使用references/market-template.csv模板准备数据")
        sys.exit(1)
    
    # 数据预处理
    df['时间戳'] = pd.to_datetime(df['时间戳'])
    df['小时'] = df['时间戳'].dt.hour
    df['供需缺口'] = df['需求(MW)'] - df['供应(MW)']
    
    # 特征工程
    X = df[['小时', '供需缺口', '温度(℃)']].values
    y = df['价格(元/MWh)'].values
    
    # 训练简单线性模型
    model = LinearRegression()
    model.fit(X, y)
    
    # 预测未来3小时
    last_hour = df['小时'].iloc[-1]
    forecast_hours = [(last_hour + i) % 24 for i in range(1, 4)]
    
    # 假设供需缺口和温度保持最近趋势
    last_gap = df['供需缺口'].iloc[-1]
    last_temp = df['温度(℃)'].iloc[-1]
    
    print("\n==== 价格预测结果 ====")
    predictions = []
    for hour in forecast_hours:
        # 简单趋势外推
        predicted_price = model.predict([[hour, last_gap, last_temp]])[0]
        predictions.append(predicted_price)
        print(f"{hour}:00 预测价格: {predicted_price:.2f} 元/MWh")
    
    # 生成交易建议
    avg_price = np.mean(predictions)
    current_price = df['价格(元/MWh)'].iloc[-1]
    
    print("\n==== 交易建议 ====")
    if avg_price > current_price * 1.05:
        print("建议: 买入远期合约 (预计价格上涨)")
    elif avg_price < current_price * 0.95:
        print("建议: 卖出或观望 (预计价格下跌)")
    else:
        print("建议: 保持当前头寸 (市场稳定)")
    
    # 风险评估
    volatility = np.std(predictions) / avg_price
    print(f"\n风险评估: 预计波动率 {volatility*100:.1f}%")
    if volatility > 0.1:
        print("警告: 市场波动性高，建议设置止损位")

if __name__ == "__main__":
    main()