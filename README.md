# 复盘分析工具

## 概览

* `复盘分析工具` 协助演训人员分析演训事件并复现演训过程。

## 快速开始
应用包含数据预处理和数据绘制两个部份。

（1）数据预处理
- 执行motion-graph.py脚本，输入原始数据文件（MetricaTrackingData.csv）和时间窗口。 
- 保存处理结果为json文件（abc.json），该json可以直接plotly绘图。

（2）事件查看和复盘
- 运行app.py脚本，可以选择前面生成的json文件（abc.json），重放演训复盘。
- 运行app.py脚本，还可以看到雷达图及不同参训方的评估指标图。


## 致谢
原始数据来自：https://github.com/metrica-sports/sample-data. 