import argparse

def compound_interest_calculator(principal, rate, time, compounds_per_year=1):
    """
    计算复利
    
    参数:
    principal: 本金
    rate: 年利率 (百分比)
    time: 时间 (年)
    compounds_per_year: 每年复利次数 (默认为1,即每年复利一次)
    
    返回:
    最终金额
    """
    rate_decimal = rate / 100
    amount = principal * (1 + rate_decimal / compounds_per_year) ** (compounds_per_year * time)
    return amount

def get_input_from_user():
    """交互式获取用户输入"""
    print("\n=== 复利计算器 ===\n")
    
    while True:
        try:
            principal = float(input("请输入本金 (¥): "))
            if principal <= 0:
                print("本金必须大于0，请重新输入")
                continue
            break
        except ValueError:
            print("请输入有效的数字")
    
    while True:
        try:
            annual_rate = float(input("请输入年利率 (%): "))
            if annual_rate < 0:
                print("利率不能为负数，请重新输入")
                continue
            break
        except ValueError:
            print("请输入有效的数字")
    
    while True:
        try:
            years = float(input("请输入时间 (年): "))
            if years <= 0:
                print("时间必须大于0，请重新输入")
                continue
            break
        except ValueError:
            print("请输入有效的数字")
    
    while True:
        try:
            compounds = int(input("请输入每年复利次数 (默认为1): ") or "1")
            if compounds <= 0:
                print("复利次数必须大于0，请重新输入")
                continue
            break
        except ValueError:
            print("请输入有效的整数")
    
    return principal, annual_rate, years, compounds

def display_result(principal, rate, time, compounds_per_year, amount):
    """显示计算结果"""
    interest = amount - principal
    print("\n" + "="*50)
    print("计算结果:")
    print("="*50)
    print(f"本金: ¥{principal:,.2f}")
    print(f"年利率: {rate}%")
    print(f"时间: {time}年")
    print(f"每年复利次数: {compounds_per_year}次")
    print(f"最终金额: ¥{amount:,.2f}")
    print(f"利息: ¥{interest:,.2f}")
    print("="*50 + "\n")

# 主程序
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='复利计算器 - 计算你的投资增长情况')
    parser.add_argument('--principal', type=float, help='本金 (¥)')
    parser.add_argument('--rate', type=float, help='年利率 (百分比)')
    parser.add_argument('--time', type=float, help='投资时间 (年)')
    parser.add_argument('--compounds', type=int, default=1, help='每年复利次数 (默认为1)')
    
    args = parser.parse_args()
    
    # 如果命令行参数都提供了，则使用命令行参数
    if args.principal is not None and args.rate is not None and args.time is not None:
        principal = args.principal
        annual_rate = args.rate
        years = args.time
        compounds_per_year = args.compounds
    else:
        # 否则进行交互式输入
        principal, annual_rate, years, compounds_per_year = get_input_from_user()
    
    # 计算并显示结果
    amount = compound_interest_calculator(principal, annual_rate, years, compounds_per_year)
    display_result(principal, annual_rate, years, compounds_per_year, amount)

####随便加一句话！312321