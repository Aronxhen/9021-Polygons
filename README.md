# 9021 Polygons

### 项目介绍：
开发了一个多边形处理与分析系统，通过读取输入文件中的网格数据，识别并处理多边形，计算其周长、面积、凸性及旋转不变性。该系统可运用于计算几何领域。例如，可用于机器人路径规划和游戏开发中的几何计算。

### 项目组成：
- Assignment_2.pdf 项目说明文档
- polygons.py 主代码
- test_polygons.py 测试代码
- polys_1.txt - polys_4.txt 测试文本
- incorret_1.txt - incorrect_2.txt 测试文本

### 测试项目指令：
1.运行测试指令  

`python test_polygons.py input_file`  

参数：  
- input_file 输入文本（全部由0和1组成）
- 输出  
  “Polygon 1:  
    Perimeter: 78.4  
    Area: 384.16  
    Convex: yes  
    Nb of invariant rotations: 4  
    Depth: 0“  
  .............
  
  输出所有多边形的相关数据（Perimeter周长，Area面积，Convex凹凸性，Nb of invariant rotations旋转不变性，Depth深度）  
  生成LaTex文件，可视化多边形  
