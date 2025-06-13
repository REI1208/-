# 基于大数据的象棋人工智能

目标：基于大数据的象棋人工智能。
人类作为红方先走棋，AI作为黑方根据人类走棋后的棋局状态做出相应的走棋策略，以尽可能战胜人类为依据。

## 项目基于

https://github.com/jynba/chess_project

本项目主要补充后端与数据集，注意：数据格式为

"chessboardStatus","predictAction",  "chessboardStatusAfterPredictAction"

当前棋盘状态：64位数字，表示当前棋盘状态

预测动作：4位数字，棋子移动前与移动后的坐标

预测后期盼状态：64位数字，移动后棋盘状态。

Kaggle:https://www.kaggle.com/datasets/boyofans/onlinexiangqi

由于Kaggle数据集使用的是WXF记谱法，建议写个脚本做格式的转化。

或者使用爬虫爬取以数字字符串表示棋盘状态的网站的棋谱，比如东萍象棋http://www.dpxq.com/

## 主要工作
* 前端：
使用框架：zh-chess、Element-plus

导入zh-chess框架：npm i zh-chess canvas -D

具体实现：在onMounted生命周期中实例化对象game，监听move、over等状态，在MoveCallback回调中执行update方法更新棋盘

在前端中，预测下一步的逻辑首先会调用后端代码搭建的预测接口，如果失败则会改为请求中国象棋云库API接口

https://www.chessdb.cn/cloudbook_api.html

如果两者都没有对应的棋谱，则会提示进入pvp状态。

* 后端
框架选择：FastAPI （FastAPI 是一个用于构建 API 的现代、快速（高性能）的 web 框架）

pandas 读取、过滤和写入 CSV 数据 
主要设计了三个接口，其中学习接口未完善

1. GET /
 return {"message": "Welcome to the Chess Predictor API"}
功能：健康检查接口，访问根路径 / 返回欢迎信息。
用处：确认服务是否已启动。

2. GET /predictChessAction/{chessboard_status}

  (核心接口，预测下一步的走法)

  🔧 主要流程：
  从 chessboard.csv 中读取数据（假设格式如下）：
  chessboard_statuspredict_actionchessboard_status_after
  筛选出所有棋盘状态匹配的行
  统计各个 predict_action 出现的频率
  返回按频率排序后的预测结果列表：

3. POST /recordChessStatus（学习功能，但是未完善，检查学习的记录就知道了）
  🔧 接收 JSON 请求体：
  json
  {
    "chessboardStatus": "0919...",
    "predictAction": "8685",
    "chessboardStatusAfterPredictAction": "1928..."
  }
  ✍ 功能：
  将一条记录追加写入 chessboard.csv 文件。
  • 后端成功收到参数后会将收到的数据写入chessboard.csv文件。

## 如何开始
1. 克隆本仓库
2. 进入项目目录

前端

```
npm install

npm run dev
```

后端

```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```


## 贡献与许可

欢迎贡献！如果你有改进或新功能的想法，请提交 pull request。

本项目基于 MIT 许可证 进行开源。

