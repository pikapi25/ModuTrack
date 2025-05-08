import pandas as pd
import matplotlib.pyplot as plt
import os
import re

def collect_e_eff_data(root_folder, r2_threshold=0.85):
    """收集所有材料的E_eff数据，并筛选R² >= 0.85的结果"""
    data = []
    low_quality_data = []
    materials = ['pink', 'white', 'yellow']
    
    for material in materials:
        material_folder = os.path.join(root_folder, material)
        for root, dirs, files in os.walk(material_folder):
            for file in files:
                if file.endswith('_hertz_results.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        # 提取 E_eff 和 R²
                        E_eff = float(re.search(r"E_eff = ([\d\.e\+-]+)", lines[0]).group(1))
                        R_squared = float(re.search(r"R² = ([\d\.e\+-]+)", lines[1]).group(1))
                        
                        # 根据 R² 过滤数据
                        if R_squared >= r2_threshold:
                            data.append((material, E_eff, R_squared))
                        else:
                            low_quality_data.append((file_path, R_squared))
    
    # 创建 DataFrame
    df = pd.DataFrame(data, columns=['Material', 'E_eff', 'R_squared'])
    
    # 保存拟合差的数据到txt
    low_quality_path = os.path.join(root_folder, 'low_quality_results.txt')
    with open(low_quality_path, 'w', encoding='utf-8') as f:
        for path, r2 in low_quality_data:
            f.write(f"{path}: R² = {r2:.4f}\n")
    print(f"低质量拟合结果已保存到 {low_quality_path}")
    
    return df

def plot_e_eff_data(df, output_path):
    """绘制并保存散点图"""
    colors = {'pink': 'red', 'white': 'blue', 'yellow': 'orange'}
    plt.figure(figsize=(8, 6))
    
    for material, color in colors.items():
        material_data = df[df['Material'] == material]
        plt.scatter(material_data.index, material_data['E_eff'], c=color, label=material, alpha=0.7)

    plt.xlabel('Sample Index')
    plt.ylabel('E_eff (Pa)')
    plt.title('E_eff Scatter Plot for Different Materials (R² >= 0.85)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # 保存图片
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"散点图已保存到 {output_path}")

def save_average_e_eff(df, output_path):
    """计算平均值并保存到txt"""
    averages = df.groupby('Material')['E_eff'].mean()
    
    # 保存到 txt 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        for material, avg in averages.items():
            f.write(f"{material}: {avg:.4e} Pa\n")
    print(f"平均值已保存到 {output_path}")

if __name__ == "__main__":
    root_folder = r"C:\Users\15546\Desktop\0506"  # 修改为你的实际路径
    
    # 1. 收集数据并筛选
    df = collect_e_eff_data(root_folder)
    
    # 2. 绘制并保存散点图
    plot_e_eff_data(df, os.path.join(root_folder, 'E_eff_scatter_plot.png'))
    
    # 3. 保存平均值
    save_average_e_eff(df, os.path.join(root_folder, 'average_E_eff_results_filtered.txt'))
