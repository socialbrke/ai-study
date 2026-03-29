#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复利计算器图形界面版本
使用Tkinter构建GUI，提供更友好的交互体验。
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# 导入现有计算函数
sys.path.append(os.path.dirname(__file__))
try:
    from test import compound_interest_calculator
except ImportError:
    # 如果导入失败，直接定义函数（备用）
    def compound_interest_calculator(principal, rate, time, compounds_per_year=1):
        """
        计算复利
        """
        rate_decimal = rate / 100
        amount = principal * (1 + rate_decimal / compounds_per_year) ** (compounds_per_year * time)
        return amount

class CompoundInterestGUI:
    """主GUI类"""
    def __init__(self, root):
        self.root = root
        self.root.title("复利计算器")
        self.root.geometry("500x600")
        self.root.resizable(True, True)
        
        # 设置样式
        self.setup_styles()
        # 创建界面
        self.create_widgets()
    
    def setup_styles(self):
        """配置样式"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('微软雅黑', 16, 'bold'))
        style.configure('Header.TLabel', font=('微软雅黑', 12, 'bold'))
        style.configure('TEntry', font=('微软雅黑', 11))
        style.configure('TButton', font=('微软雅黑', 11))
        style.configure('Result.TLabel', font=('微软雅黑', 12))
    
    def create_widgets(self):
        """创建所有界面组件"""
        # 标题
        title_label = ttk.Label(self.root, text="复利计算器", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # 输入框架
        input_frame = ttk.Frame(self.root, padding="20")
        input_frame.pack(fill='both', expand=True)
        
        # 本金
        self.create_input_field(input_frame, "本金 (¥):", "principal", 0)
        # 年利率
        self.create_input_field(input_frame, "年利率 (%):", "rate", 1)
        # 时间（年）
        self.create_input_field(input_frame, "投资时间 (年):", "time", 2)
        # 每年复利次数
        self.create_input_field(input_frame, "每年复利次数:", "compounds", 3, default="1")
        
        # 按钮框架
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack()
        
        self.calc_button = ttk.Button(button_frame, text="计算复利", command=self.calculate)
        self.calc_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="清空输入", command=self.clear_inputs)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = ttk.Button(button_frame, text="退出", command=self.root.quit)
        self.quit_button.pack(side=tk.LEFT, padx=5)
        
        # 结果显示框架
        result_frame = ttk.LabelFrame(self.root, text="计算结果", padding="15")
        result_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        self.result_labels = {}
        fields = [
            ("本金:", "principal_result"),
            ("年利率:", "rate_result"),
            ("投资时间:", "time_result"),
            ("每年复利次数:", "compounds_result"),
            ("最终金额:", "amount_result"),
            ("利息:", "interest_result")
        ]
        
        for i, (text, key) in enumerate(fields):
            label = ttk.Label(result_frame, text=text, style='Header.TLabel')
            label.grid(row=i, column=0, sticky='w', pady=5, padx=5)
            value_label = ttk.Label(result_frame, text="", style='Result.TLabel')
            value_label.grid(row=i, column=1, sticky='w', pady=5, padx=5)
            self.result_labels[key] = value_label
        
        # 底部说明
        note = ttk.Label(self.root, text="提示：输入数字，点击“计算复利”按钮获得结果。", font=('微软雅黑', 9))
        note.pack(pady=10)
    
    def create_input_field(self, parent, label_text, field_name, row, default=""):
        """创建标签和输入框的组合"""
        label = ttk.Label(parent, text=label_text, style='Header.TLabel')
        label.grid(row=row, column=0, sticky='w', pady=10, padx=5)
        
        entry = ttk.Entry(parent, width=25)
        entry.grid(row=row, column=1, sticky='w', pady=10, padx=5)
        if default:
            entry.insert(0, default)
        setattr(self, f"{field_name}_entry", entry)
    
    def get_input_value(self, field_name):
        """从输入框获取值，返回浮点数或整数"""
        entry = getattr(self, f"{field_name}_entry")
        value_str = entry.get().strip()
        if not value_str:
            return None
        try:
            if field_name == "compounds":
                return int(value_str)
            else:
                return float(value_str)
        except ValueError:
            return None
    
    def calculate(self):
        """执行计算并更新结果"""
        # 获取输入值
        principal = self.get_input_value("principal")
        rate = self.get_input_value("rate")
        time = self.get_input_value("time")
        compounds = self.get_input_value("compounds")
        
        # 验证输入
        errors = []
        if principal is None or principal <= 0:
            errors.append("本金必须是一个大于0的数字")
        if rate is None or rate < 0:
            errors.append("年利率必须是一个非负数")
        if time is None or time <= 0:
            errors.append("投资时间必须是一个大于0的数字")
        if compounds is None or compounds <= 0:
            errors.append("每年复利次数必须是一个大于0的整数")
        
        if errors:
            messagebox.showerror("输入错误", "\n".join(errors))
            return
        
        # 计算
        amount = compound_interest_calculator(principal, rate, time, compounds)
        interest = amount - principal
        
        # 更新结果标签
        self.result_labels["principal_result"].config(text=f"¥{principal:,.2f}")
        self.result_labels["rate_result"].config(text=f"{rate}%")
        self.result_labels["time_result"].config(text=f"{time} 年")
        self.result_labels["compounds_result"].config(text=f"{compounds} 次/年")
        self.result_labels["amount_result"].config(text=f"¥{amount:,.2f}")
        self.result_labels["interest_result"].config(text=f"¥{interest:,.2f}")
    
    def clear_inputs(self):
        """清空所有输入框"""
        for field in ["principal", "rate", "time", "compounds"]:
            entry = getattr(self, f"{field}_entry")
            entry.delete(0, tk.END)
            if field == "compounds":
                entry.insert(0, "1")
        
        # 清空结果
        for label in self.result_labels.values():
            label.config(text="")

def main():
    """启动GUI"""
    root = tk.Tk()
    app = CompoundInterestGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()