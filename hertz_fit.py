import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os
import re
from pathlib import Path

def hertz_fit_and_save(root_folder, retract_csv_path, R=10e-6):
    """执行Hertz拟合并保存结果"""

    # 读取retract数据
    df = pd.read_csv(retract_csv_path)
    displacement_nm = df.iloc[:, 0].values
    force_uN = df.iloc[:, 1].values

    # 单位转换
    displacement = displacement_nm * 1e-9  # nm → m
    force = force_uN * 1e-6               # μN → N

    # Hertz模型
    def hertz_model(delta, E_eff):
        return (4/3) * E_eff * np.sqrt(R) * delta**1.5

    # 曲线拟合
    popt, _ = curve_fit(hertz_model, displacement, force, bounds=(0, np.inf))
    E_eff = popt[0]

    # 计算R²
    force_pred = hertz_model(displacement, E_eff)
    residuals = force - force_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((force - np.mean(force))**2)
    r_squared = 1 - (ss_res / ss_tot)

    
    # 保存结果到文本文件
    timestamp = re.search(r'(\d{8}_\d{6})', retract_csv_path).group(1)
    output_filename = f"{timestamp}_hertz_results.txt"
    result_text = f"E_eff = {E_eff:.4e} Pa\nR² = {r_squared:.4f}\nR = {R*1e6:.2f} μm"
    result_file = os.path.join(root_folder, output_filename)
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write(result_text)
    print(f"结果已保存到 {result_file}")

    # 绘制并保存图像
    delta_fit = np.linspace(min(displacement), max(displacement), 200)
    force_fit = hertz_model(delta_fit, E_eff)

    plt.figure(figsize=(10, 6))
    plt.plot(displacement * 1e9, force * 1e6, 'bo', markersize=4, label='exp data')
    plt.plot(delta_fit * 1e9, force_fit * 1e6, 'r-', linewidth=2, label='Hertz fitting curve')
    plt.xlabel('displacement (nm)', fontsize=12)
    plt.ylabel('force (μN)', fontsize=12)
    plt.title(f'Hertz fitting result (R² = {r_squared:.4f})', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plot_file = os.path.join(root_folder, f"{timestamp}_hertz_fit.png")
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"拟合图已保存到 {plot_file}")

    return E_eff, r_squared


def batch_process_hertz_fit(root_folder, R=10e-6):
    """批量处理所有retract数据文件"""
    print(f"开始批量处理Hertz拟合, 压头半径 R = {R*1e6:.2f} μm...")
    
    # 遍历所有子文件夹
    for root, dirs, files in os.walk(root_folder):
        # 查找所有retract数据文件
        retract_files = [f for f in os.listdir(root) if f.endswith('_retract_data.csv')]
        for file in retract_files:
            file_path = os.path.join(root, file)
            print(f"\n处理文件: {file_path}")
            # 执行Hertz拟合
            E_eff, r_squared = hertz_fit_and_save(root, file_path, R)
            
if __name__ == "__main__":
    # 设置根文件夹路径
    root_folder = r"C:\Users\15546\Desktop\0506\yellow"  # 修改为你的实际路径
    
    # 开始批量处理
    print("开始批量fit数据...")
    batch_process_hertz_fit(root_folder)
    print("\n所有处理完成!")