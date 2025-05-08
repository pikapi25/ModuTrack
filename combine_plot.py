import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import math

def combine_experiment_plots(root_folder, output_folder):
    """合并同一材料的实验图"""
    materials = ['pink', 'white', 'yellow']
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for material in materials:
        print(f"正在处理 {material} 的实验图...")
        material_folder = os.path.join(root_folder, material)
        
        # 收集所有 Hertz 拟合图片路径
        image_paths = []
        experiment_names = []
        
        for root, dirs, files in os.walk(material_folder):
            for file in files:
                if file.endswith('_hertz_fit.png'):
                    image_paths.append(os.path.join(root, file))
                    experiment_name = os.path.basename(root)  # 文件夹名字代表实验名
                    experiment_names.append(experiment_name)

        # 按实验名称排序，保证顺序一致
        image_paths, experiment_names = zip(*sorted(zip(image_paths, experiment_names)))
        
        # 计算网格大小
        num_images = len(image_paths)
        cols = 3
        rows = math.ceil(num_images / cols)
        
        # 创建画布
        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
        axes = axes.flatten()  # 展开成一维数组，方便索引
        
        for i, (img_path, exp_name) in enumerate(zip(image_paths, experiment_names)):
            img = mpimg.imread(img_path)
            axes[i].imshow(img)
            axes[i].set_title(exp_name, fontsize=10)
            axes[i].axis('off')
        
        # 删除多余的子图
        for j in range(i + 1, len(axes)):
            axes[j].axis('off')

        # 保存拼接后的图片
        combined_image_path = os.path.join(output_folder, f"{material}_combined.png")
        plt.tight_layout()
        plt.savefig(combined_image_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"{material} 的拼接图已保存到 {combined_image_path}")

if __name__ == "__main__":
    root_folder = r"C:\Users\15546\Desktop\0506"      # 修改为你的实验数据路径
    output_folder = os.path.join(root_folder, "combined_plots")  # 输出路径
    
    # 执行图片合并
    combine_experiment_plots(root_folder, output_folder)
