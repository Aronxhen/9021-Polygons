from polygons import Polygons
import sys

def main():
    # 输入文件名
    if sys.argv[1]:
        input_file = sys.argv[1]  # 确保文件路径正确
    else:
        exit(1)

    try:
        # 创建 Polygons 对象
        polygons = Polygons(input_file)
        
        # 调用 analyse 方法，打印每个多边形的信息
        print("分析结果：")
        polygons.analyse()
        
        # 调用 display 方法，生成 LaTeX 文件
        print("正在生成 LaTeX 文件...")
        polygons.display()
        print(f"LaTeX 文件生成完成：{input_file.replace('.txt', '.tex')}")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
