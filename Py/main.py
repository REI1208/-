from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()
CSV_FILE = "chessboard.csv"

# 允许跨域的域名列表，比如前端地址
origins = [
    "http://localhost:3000",  # 你的前端地址，端口换成你实际用的
    "http://localhost:5173",
    "http://47.107.108.89:4001"
    # 可以添加其他允许的域名
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许跨域的来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法
    allow_headers=["*"],  # 允许所有请求头
)

# 你的数据模型和路由不变
class ChessRecord(BaseModel):
    chessboardStatus: str
    predictAction: str
    chessboardStatusAfterPredictAction: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Chess Predictor API"}

@app.get("/predictChessAction/{chessboard_status}")
def predict_chess_action(chessboard_status: str):
    if not os.path.exists(CSV_FILE):
        return {"predictions": []}

    try:
        df = pd.read_csv(CSV_FILE)
    except Exception as e:
        return {"error": f"读取文件失败: {str(e)}"}

    df_filtered = df[df["chessboard_status"] == chessboard_status]

    if df_filtered.empty:
        return {"predictions": []}

    result = (
        df_filtered.groupby("predict_action")
        .size()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
    )

    predictions = result.to_dict(orient="records")
    return {"predictions": predictions}

@app.post("/recordChessStatus")
def record_chess_status(record: ChessRecord):
    new_data = pd.DataFrame([{
        "chessboard_status": record.chessboardStatus,
        "predict_action": record.predictAction,
        "chessboard_status_after": record.chessboardStatusAfterPredictAction
    }])

    file_exists = os.path.exists(CSV_FILE)
    new_data.to_csv(CSV_FILE, mode='a', header=not file_exists, index=False)

    return {"message": "Record saved successfully"}
