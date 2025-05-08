import pandas as pd
import os
import re
import matplotlib.pyplot as plt
from pathlib import Path

def plot_retract_data(df, output_path, timestamp):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Indentation'], df['Force'], 'b-', linewidth=1)
    plt.xlabel('Indentation (nm)', fontsize=12)
    plt.ylabel('Force (μN)', fontsize=12)
    plt.title(f'Retract Curve ({timestamp})', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # 设置坐标轴从0开始
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    
    # 保存图像
    plot_filename = os.path.join(output_path, f"{timestamp}_retract_plot.png")
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"曲线图已保存到 {plot_filename}")

def process_retract_data(folder_path):
    # 查找符合条件的fz_data文件和cp文件
    fz_files = [f for f in os.listdir(folder_path) if f.endswith('_fz_data.csv')]
    cp_files = [f for f in os.listdir(folder_path) if f.lower() == 'cp.txt']
    
    if not fz_files:
        print(f"未找到_fz_data.csv文件在 {folder_path}")
        return
    if not cp_files:
        print(f"未找到cp.txt文件在 {folder_path}")
        return
    
    # 使用第一个匹配的fz文件
    fz_data_path = os.path.join(folder_path, fz_files[0])
    cp_file_path = os.path.join(folder_path, cp_files[0])
        
    # 读取fz数据
    df = pd.read_csv(fz_data_path)
    
    # 读取接触点
    with open(cp_file_path, 'r') as f:
        cp_value = float(f.read().strip())
    
    # 找到最高点索引
    max_force_idx = df['Line0004Point0000Force'].idxmax()
    
    # 找到接触点最近的索引
    cp_idx = (df['Line0004Point0000Ind_Ext'] - cp_value).abs().idxmin()
    
    # 提取cp到最高点之间的数据
    retract_df = df.iloc[max_force_idx+1:cp_idx].copy()
    
    # 数据处理：横坐标从cp点开始计算
    retract_df['Indentation'] = retract_df['Line0004Point0000Ind_Ext'] - cp_value
    # 水平翻转使曲线从左到右递增
    retract_df['Indentation'] = -retract_df['Indentation']
    retract_df['Force'] = retract_df['Line0004Point0000Force'] - df['Line0004Point0000Force'][cp_idx]
    
    # 重置索引
    retract_df.reset_index(drop=True, inplace=True)
    
    # 从原始文件名提取timestamp
    timestamp = re.search(r'(\d{8}_\d{6})', fz_files[0]).group(1)
    output_filename = f"{timestamp}_retract_data.csv"
    output_path = os.path.join(folder_path, output_filename)
    
    # 保存处理后的数据（只保留需要的列）
    retract_df[['Indentation', 'Force']].to_csv(output_path, index=False)
    print(f"处理完成，结果已保存到 {output_path}")
    
    # 绘制并保存曲线图
    plot_retract_data(retract_df, folder_path, timestamp)
    
    return retract_df
        
    # except Exception as e:
    #     print(f"处理 {folder_path} 时出错: {str(e)}")
    #     return None

def batch_process_retract_data(root_folder):
    # 遍历所有子文件夹
    for root, dirs, files in os.walk(root_folder):
        # 检查是否是实验文件夹（包含数字编号的文件夹）
        current_path = Path(root)
        if any(part.isdigit() for part in current_path.parts):
            print(f"\n处理文件夹: {root}")
            process_retract_data(root)

if __name__ == "__main__":
    # 设置根文件夹路径
    root_folder = r"C:\Users\15546\Desktop\0506\yellow"  # 修改为你的实际路径
    
    # 开始批量处理
    print("开始批量处理retract数据...")
    batch_process_retract_data(root_folder)
    print("\n所有处理完成!")