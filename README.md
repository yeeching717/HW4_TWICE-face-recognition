# TWICE 成員人臉辨識系統

## 專案說明

本專案改編自以下 GitHub 專案：
- **原始專案**：[yenlung/AI-Demo](https://github.com/yenlung/AI-Demo.git)
- **主要修改**：
  - 將 Gradio 介面改為 Streamlit
  - 分離人臉特徵資料庫建立（main.py）與遊戲介面（app.py）
  - 針對 Windows 環境解決 InsightFace 依賴問題
  - 調整為本地端運行

## 環境設定

### 使用虛擬環境

1. **啟動虛擬環境**（已建立）：
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **檢查套件是否已安裝**：
   ```powershell
   pip list
   ```

3. **如需重新安裝套件**：
   ```powershell
   pip install -r requirements.txt
   ```

### 執行程式

#### 1. 建立人臉特徵資料庫（首次執行）
```powershell
python main.py
```
這會建立人臉特徵資料庫並執行準確率測試。

#### 2. 啟動 Streamlit 遊戲介面
```powershell
streamlit run app.py
```
或使用完整路徑：
```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

然後在瀏覽器開啟顯示的網址（通常是 http://localhost:8501）

### 關閉虛擬環境

```powershell
deactivate
```

## 專案結構

```
IoTHW4/
├── venv/                      # Python 虛擬環境
├── photos/                    # 訓練照片資料夾
│   ├── cy/                    # 彩瑛
│   ├── dh/                    # 多賢
│   ├── jh/                    # 志效
│   ├── jy/                    # 定延
│   ├── mi/                    # mina
│   ├── mo/                    # momo
│   ├── ny/                    # 娜璉
│   ├── sa/                    # sana
│   └── ty/                    # 子瑜
├── test_photos/               # 測試照片資料夾（同上結構）
├── main.py                    # 人臉特徵資料庫建立程式
├── app.py                     # Streamlit 互動遊戲介面
└── requirements.txt           # 套件依賴列表
```

## 功能說明

1. **main.py**：建立人臉特徵資料庫
   - 載入 InsightFace 模型
   - 從 `photos/` 資料夾讀取訓練照片
   - 建立每位成員的人臉特徵向量
   - 使用 `test_photos/` 進行準確率測試

2. **app.py**：Streamlit 互動遊戲介面
   - 匯入 main.py 的人臉辨識功能
   - 提供網頁介面與 AI 比賽辨識 TWICE 成員
   - 即時顯示分數和結果

## 注意事項

- 確保照片資料夾結構正確
- 虛擬環境需先啟動才能執行程式
- 程式會自動開啟瀏覽器顯示 Gradio 介面
