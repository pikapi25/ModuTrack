import pandas as pd
import matplotlib.pyplot as plt
import os
import re

def convert_to_force(corrected_value):
    return (-0.000930 * (corrected_value) + 2.941133) * 0.001 * 9.8 * 10**6

def calculate_baseline(df):
    # 计算前10-30个数据点的平均值作为baseline
    start_index = 0  # 从第10个数据点开始
    end_index = 30  # 到第30个数据点结束
    
    baseline_data = df["Value"].iloc[start_index:end_index]
    baseline = baseline_data.mean()
    return baseline

def plot_force_distance(distances, forces, output_path):
    plt.figure(figsize=(10, 6))
    plt.plot(distances, forces, 'b-', linewidth=1)
    plt.xlabel('Distance (nm)', fontsize=12)
    plt.ylabel('Force (μN)', fontsize=12)
    plt.title('Force-Distance Relationship', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    plot_filename = os.path.join(output_path, "force_distance_plot.png")
    plt.savefig(plot_filename)
    plt.close()
    print(f"Plot saved to {plot_filename}")

def data_format_transfer(input_csv, output_path):
    # 检查是否是已处理的文件，避免重复处理
    if "_fz_data.csv" in input_csv or "processed_data.csv" in input_csv:
        print(f"Skipping already processed file: {input_csv}")
        return

    try:
        # 读取原始CSV数据
        df = pd.read_csv(input_csv)
        
        # 检查是否包含必要的列
        if "Time (s)" not in df.columns or "Value" not in df.columns:
            print(f"File {input_csv} doesn't contain required columns ('Time (s)' and 'Value')")
            return

        # 确保数据按时间升序排列
        df = df.sort_values(by="Time (s)")
        min_time = df["Time (s)"].iloc[0]
        df["Time (s)"] = df["Time (s)"] - min_time

        # 计算baseline
        baseline = calculate_baseline(df)
        print(f"Calculated baseline for {input_csv}: {baseline}")

        # 去皮处理，并转换为力
        corrected_values = []
        forces = []
        distances = []

        for index, row in df.iterrows():
            time = row["Time (s)"]
            value = row["Value"]
            
            # 去皮：减去 baseline
            corrected_value = value - baseline
            corrected_values.append(corrected_value)
            
            # 将去皮后的值转换为力
            force = convert_to_force(corrected_value)
            forces.append(force)
            
            # 计算距离：时间乘以速度 (0.0325 mm/s)
            distance = time * 0.0325 * 10**(-3) * 10**9  # 速度是 0.0325 mm/s
            distances.append(distance)

        # 创建输出文件名
        input_filename = os.path.basename(input_csv)
        timestamp_match = re.search(r'(\d{8}_\d{6})', input_filename)
        timestamp = timestamp_match.group(1) if timestamp_match else "processed"
        
        # 创建新的 DataFrame 用于输出
        output_df = pd.DataFrame({
            "Line0004Point0000Ind_Ext": distances,
            "Line0004Point0000Force": forces
        })

        # 保存为新的 CSV 文件
        output_csv = os.path.join(output_path, f"{timestamp}_fz_data.csv")
        output_df.to_csv(output_csv, index=False)
        print(f"Data saved to {output_csv}")

        # 生成并保存图表
        plot_force_distance(distances, forces, output_path)

    except Exception as e:
        print(f"Error processing {input_csv}: {str(e)}")

def process_all_experiments(root_folder):
    # 遍历所有子目录
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith("data.csv") and not file.endswith("_fz_data.csv"):
                input_csv = os.path.join(root, file)
                print(f"\nProcessing {input_csv}")
                data_format_transfer(input_csv, root)

if __name__ == "__main__":
    # 设置包含所有实验数据的根文件夹
    root_folder = r"C:\Users\15546\Desktop\0506"  # 更新此路径
    
    # 处理子文件夹中的所有实验
    process_all_experiments(root_folder)
    
    print("\nBatch processing completed!")