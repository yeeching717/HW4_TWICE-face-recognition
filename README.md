# TWICE 成員人臉辨識系統 🎭

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hw4-twice-face-recognition.streamlit.app/)

## 📝 專案說明

本專案是一個基於深度學習的 TWICE 成員人臉辨識系統，使用者可以與 AI 比賽，看誰更能準確辨識 TWICE 成員！

**線上體驗**：[https://hw4-twice-face-recognition.streamlit.app/](https://hw4-twice-face-recognition.streamlit.app/)

### 專案來源

本專案改編自 [yenlung/AI-Demo](https://github.com/yenlung/AI-Demo) 的人臉辨識示範：
- **原始 Notebook**：[和AI_PK看誰比較會認TWICE成員.ipynb](https://github.com/yenlung/AI-Demo/blob/master/%E3%80%90Demo03v%E3%80%91%E5%92%8CAI_PK%E7%9C%8B%E8%AA%B0%E6%AF%94%E8%BC%83%E6%9C%83%E8%AA%8DIVE%E6%88%90%E5%93%A1.ipynb)

### 主要改進

- ✅ 將 Jupyter Notebook 重構為模組化的 Python 專案
- ✅ 從 Gradio 改為 Streamlit 網頁介面
- ✅ 分離關注點：資料處理（main.py）與使用者介面（app.py）
- ✅ 支援 Windows 本地端開發環境
- ✅ 部署至 Streamlit Cloud，支援線上體驗
- ✅ 解決 InsightFace 在不同環境的依賴問題

## 🚀 快速開始

### 線上使用

直接訪問：[https://hw4-twice-face-recognition.streamlit.app/](https://hw4-twice-face-recognition.streamlit.app/)

### 本地端安裝

#### 環境需求

- Python 3.9+ (本地開發) 或 Python 3.13 (雲端部署)
- Windows (本地) / Linux (Streamlit Cloud)

#### 安裝步驟

1. **複製專案**
   ```bash
   git clone https://github.com/yeeching717/HW4_TWICE-face-recognition.git
   cd HW4_TWICE-face-recognition
   ```

2. **建立虛擬環境**（Windows）
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **安裝依賴套件**
   ```powershell
   pip install -r requirements.txt
   ```

## 💻 使用方式

### 本地端執行

#### 步驟 1：建立人臉特徵資料庫

首次執行需要先建立人臉特徵資料庫：

```powershell
python main.py
```

此步驟會：
- 自動下載 InsightFace 的 `buffalo_l` 模型（約 500MB）
- 從 `photos/` 資料夾讀取 TWICE 成員照片
- 提取人臉特徵並建立特徵向量資料庫
- 使用 `test_photos/` 測試集計算辨識準確率

**預期輸出**：
```
正在載入 InsightFace 模型...
模型載入完成！
正在建立人臉特徵資料庫...
已處理 61 張照片
測試準確率：88.9% (16/18)
```

#### 步驟 2：啟動 Streamlit 遊戲介面

```powershell
streamlit run app.py
```

瀏覽器會自動開啟 `http://localhost:8501`

### 線上使用

直接訪問 [Streamlit Cloud 部署版本](https://hw4-twice-face-recognition.streamlit.app/)，無需安裝！

## 📁 專案結構

```
HW4_TWICE-face-recognition/
├── .streamlit/
│   └── config.toml           # Streamlit 配置（Python 版本等）
├── photos/                   # 訓練照片資料夾（61 張）
│   ├── cy/                   # 彩瑛 (Chaeyoung)
│   ├── dh/                   # 多賢 (Dahyun)
│   ├── jh/                   # 志效 (Jihyo)
│   ├── jy/                   # 定延 (Jeongyeon)
│   ├── mi/                   # Mina
│   ├── mo/                   # Momo
│   ├── ny/                   # 娜璉 (Nayeon)
│   ├── sa/                   # Sana
│   └── ty/                   # 子瑜 (Tzuyu)
├── test_photos/              # 測試照片資料夾（18 張，同上結構）
├── main.py                   # 人臉特徵資料庫建立與辨識核心
├── app.py                    # Streamlit 互動遊戲介面
├── requirements.txt          # Python 套件依賴
├── runtime.txt               # Python 版本指定（Streamlit Cloud）
├── packages.txt              # 系統依賴（Streamlit Cloud）
├── .gitignore                # Git 忽略規則
└── README.md                 # 專案說明文件
```

## 🎮 功能說明

### main.py - 人臉辨識核心

**主要功能：**
- 使用 InsightFace 的預訓練模型進行人臉檢測與特徵提取
- 建立 TWICE 九位成員的人臉特徵向量資料庫
- 提供人臉辨識函數供 Streamlit 介面呼叫
- 測試集準確率評估

**關鍵函數：**
- `build_database()`: 建立人臉特徵資料庫
- `recognize_face(image)`: 辨識照片中的 TWICE 成員
- `display_test_results()`: 顯示測試結果與準確率

### app.py - Streamlit 互動介面

**遊戲玩法：**
1. 系統從測試集隨機選取照片
2. AI 使用人臉辨識模型進行預測
3. 使用者猜測照片中的成員
4. 比較 AI 和使用者的答案
5. 計算雙方的正確率和得分

**功能特色：**
- 📊 即時顯示 AI 預測結果與信心度
- 🏆 計分系統與準確率統計
- 🔄 遊戲重置功能
- 📈 側邊欄顯示遊戲統計資訊

## 🛠️ 技術架構

### 核心技術

- **深度學習框架**: [InsightFace](https://github.com/deepinsight/insightface) - 人臉辨識
- **模型**: buffalo_l (ArcFace + RetinaFace)
- **推論引擎**: ONNX Runtime
- **前端框架**: Streamlit
- **影像處理**: OpenCV, Pillow
- **數值計算**: NumPy, SciPy

### 依賴套件

主要套件版本（詳見 `requirements.txt`）：

```
streamlit              # Web 介面框架
insightface>=0.7.3     # 人臉辨識模型
onnxruntime            # ONNX 模型推論引擎
opencv-python-headless # 影像處理（無 GUI）
numpy>=2.0.0           # 數值計算
albumentations>=1.3.0  # 影像增強
```

### 部署配置

**Streamlit Cloud 配置檔案：**

- `runtime.txt`: Python 版本（3.13.1）
- `packages.txt`: 系統依賴（libgl1, libglib2.0-0）
- `.streamlit/config.toml`: Streamlit 伺服器配置

## 🎯 模型效能

**測試集結果：**
- 測試照片數量：18 張（每位成員 2 張）
- 辨識準確率：**88.9%** (16/18)
- 錯誤案例：2 張（通常為側臉或低解析度）

**模型特性：**
- 模型大小：約 500MB
- 推論速度：< 1 秒/張（CPU）
- 支援多人臉檢測
- 信心度閾值：0.4

## 🔧 開發說明

### 本地開發環境

```powershell
# 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 執行測試
python main.py

# 啟動開發伺服器
streamlit run app.py

# 關閉虛擬環境
deactivate
```

### 新增訓練資料

1. 將新照片放入 `photos/<member_code>/` 資料夾
2. 重新執行 `python main.py` 建立資料庫
3. 將測試照片放入 `test_photos/<member_code>/`

### 雲端部署

本專案已配置自動部署至 Streamlit Cloud：

1. 推送程式碼至 GitHub
2. Streamlit Cloud 自動檢測更新
3. 自動重新部署應用程式

**注意事項：**
- 模型檔案不包含在 Git 中（太大），首次執行會自動下載
- Streamlit Cloud 使用 Linux 環境，需使用 `opencv-python-headless`

## ⚠️ 疑難排解

### Windows 環境問題

**問題：stringzilla 編譯失敗**

解決方案：使用 `insightface==0.6.2` 或降級相關套件

**問題：虛擬環境啟動失敗**

解決方案：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Streamlit Cloud 部署問題

**問題：Python 版本不相容**

確保 `runtime.txt` 存在且格式正確：
```
python-3.13.1
```

**問題：套件安裝失敗**

檢查 `requirements.txt` 版本相容性，使用版本範圍而非固定版本

## 📄 授權聲明

本專案改編自 [yenlung/AI-Demo](https://github.com/yenlung/AI-Demo)，僅供學習與研究使用。

- TWICE 成員照片版權歸 JYP Entertainment 所有
- InsightFace 模型遵循其原始授權條款
- 程式碼部分採用 MIT License

## 🙏 致謝

- 原始專案作者：[yenlung](https://github.com/yenlung)
- InsightFace 團隊提供的強大人臉辨識模型
- Streamlit 團隊提供的優秀 Web 框架
- TWICE 成員提供靈感 ✨

## 📧 聯絡方式

如有問題或建議，歡迎透過 GitHub Issues 回報。
