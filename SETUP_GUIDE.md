# TWICE 成員人臉辨識系統 - 詳細說明

## 專案概述

這是一個基於 InsightFace 深度學習模型的 TWICE 成員人臉辨識系統，使用 Gradio 提供互動式網頁介面。

## 安裝與設定過程記錄

### 遇到的問題與解決方案

#### 問題 1: stringzilla 編譯失敗

**錯誤訊息**:
```
ERROR: Failed building wheel for stringzilla
error: command 'cl.exe' failed with exit code 2
```

**原因**:
- `stringzilla` 套件需要 C11 編譯器
- Windows MSVC 編譯器無法正確編譯其 UTF-8 處理程式碼
- 中文 locale (code page 950) 導致額外的警告

**影響範圍**:
- `albumentations 2.0+` 依賴 `stringzilla>=3.10.4`
- `insightface 0.7.3` 依賴 `albumentations`

**解決方案**:
1. 降級到 InsightFace 0.6.2 版本
2. 使用 `--no-deps` 安裝 InsightFace，避免自動安裝 albumentations
3. 手動修改 `venv/lib/site-packages/insightface/app/mask_renderer.py`，將 albumentations 設為可選依賴

#### 問題 2: NumPy 版本衝突

**問題**: Gradio 需要 numpy<2.0，但其他套件偏好 numpy>=2.0

**解決方案**: 安裝 numpy==1.26.4

#### 問題 3: InsightFace 模型下載失敗

**錯誤訊息**:
```
RuntimeError: Failed downloading url http://insightface.cn-sh2.ufileos.com/models/buffalo_l.zip
```

**原因**: 
- 網路連線問題
- 中國伺服器連線不穩定
- 防火牆或 ISP 封鎖

**解決方案**:
1. **使用代理或 VPN**
2. **手動下載模型**:
   - 下載網址: http://insightface.cn-sh2.ufileos.com/models/buffalo_l.zip
   - 解壓縮到: `C:\Users\<你的使用者名稱>\.insightface\models\buffalo_l\`
   - 確保資料夾包含所有 .onnx 模型檔案
3. **使用備用下載源**（如果可用）

## 已安裝的套件清單

### 核心套件
- **InsightFace**: 0.6.2 - 人臉辨識模型
- **Gradio**: 3.50.2 - Web 介面框架
- **ONNX Runtime**: 1.19.2 - 模型推論引擎

### 影像處理
- **OpenCV (opencv-python)**: 4.12.0.88
- **Pillow**: 10.4.0
- **scikit-image**: 0.24.0

### 數值計算
- **NumPy**: 1.26.4
- **SciPy**: 1.13.1
- **scikit-learn**: 1.6.1

### 其他工具
- **Matplotlib**: 3.9.4 - 繪圖工具
- **tqdm**: 4.67.1 - 進度條顯示
- **requests**: 2.32.5 - HTTP 請求

## 執行步驟

### 1. 啟動虛擬環境

```powershell
.\venv\Scripts\Activate.ps1
```

你應該會看到終端提示符前面出現 `(venv)`。

### 2. 執行主程式

```powershell
python main.py
```

### 3. 程式執行流程

程式會自動執行以下步驟：

1. **載入 TWICE 成員設定** (9位成員)
2. **導入必要套件**
3. **下載 InsightFace 模型** (如果尚未下載)
   - 模型名稱: buffalo_l
   - 大小: 約 400-500 MB
   - 儲存位置: `C:\Users\<username>\.insightface\models\buffalo_l\`
4. **建立人臉特徵資料庫**
   - 讀取 `photos/` 資料夾中每位成員的照片
   - 提取人臉特徵向量
   - 顯示進度條
5. **執行測試集評估**
   - 使用 `test_photos/` 資料夾的照片
   - 計算辨識準確率
   - 顯示混淆矩陣
6. **啟動 Gradio 介面**
   - 本地網址: http://127.0.0.1:7860
   - 公開分享網址（選擇性）

### 4. 使用 Gradio 介面

打開瀏覽器訪問 `http://127.0.0.1:7860`，你會看到：

- **上傳照片**: 選擇 TWICE 成員的照片
- **AI 預測**: 系統會顯示辨識結果和信心分數
- **你的預測**: 從下拉選單選擇你的答案
- **提交**: 檢查答案並累計分數

## 檔案結構說明

### main.py

主程式包含以下功能：

1. **成員設定** (lines 13-32)
   - 資料夾名稱對應成員名稱
   - 中韓文顯示名稱

2. **模型初始化** (lines 46-51)
   - 使用 CPU 執行提供者
   - 設定偵測大小為 (640, 640)

3. **特徵提取** (lines 53-114)
   - `extract_features()`: 從單張照片提取人臉特徵
   - `build_database()`: 建立所有成員的特徵資料庫

4. **辨識函數** (lines 116-160)
   - `recognize_face()`: 使用餘弦相似度比對
   - 回傳最相似的成員和信心分數

5. **測試評估** (lines 162-222)
   - 自動測試準確率
   - 生成混淆矩陣
   - 顯示詳細統計

6. **Gradio 介面** (lines 224-391)
   - 遊戲模式
   - 計分系統
   - 互動式 UI

### photos/ 和 test_photos/

資料夾結構應為：

```
photos/
├── cy/          # 彩瑛 - 至少 5-10 張照片
│   ├── 001.jpg
│   ├── 002.jpg
│   └── ...
├── dh/          # 多賢
├── jh/          # 志效
├── jy/          # 定延
├── mi/          # mina
├── mo/          # momo
├── ny/          # 娜璉
├── sa/          # sana
└── ty/          # 子瑜
```

**照片要求**:
- 格式: JPG, PNG
- 每位成員至少 5 張照片（越多越好）
- 清晰、正面、光線充足
- 建議解析度: 至少 640x640

## 技術細節

### InsightFace 模型

- **模型架構**: buffalo_l
- **輸入**: RGB 影像，任意尺寸
- **輸出**: 512 維人臉特徵向量
- **用途**: 人臉偵測、對齊、特徵提取

### 辨識算法

使用**餘弦相似度**比對人臉特徵：

```python
similarity = cosine_similarity(feature1, feature2)
```

- 範圍: -1 到 1
- 越接近 1 表示越相似
- 閾值: 通常設定為 0.4-0.6

### Gradio 版本

使用 Gradio 3.50.2（較舊版本）原因：
- 相容性更好
- 依賴套件較少
- 避免 numpy 2.0 衝突

## 常見問題 FAQ

### Q1: 程式啟動很慢？

**A**: 首次執行需要：
- 下載模型檔案 (400-500 MB)
- 建立特徵資料庫
- 後續執行會快很多

### Q2: 辨識準確率不高？

**A**: 可能原因：
- 訓練照片太少
- 照片品質不佳（模糊、側臉、遮擋）
- 光線不足
- 建議每位成員至少 10-20 張高品質照片

### Q3: 無法啟動虛擬環境？

**A**: 
```powershell
# 如果 PowerShell 執行政策限制
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然後再次嘗試
.\venv\Scripts\Activate.ps1
```

### Q4: 出現 "No module named 'xxx'" 錯誤？

**A**: 確保虛擬環境已啟動，然後重新安裝套件：
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install --no-deps insightface==0.6.2
```

### Q5: Gradio 無法在瀏覽器開啟？

**A**: 手動複製網址到瀏覽器：
```
http://127.0.0.1:7860
```

## 進階設定

### 調整偵測閾值

在 `main.py` 中修改：

```python
# 降低閾值（更寬鬆）
det_thresh=0.3  # 原本 0.5

# 提高閾值（更嚴格）
det_thresh=0.7
```

### 使用 GPU 加速

如果有 NVIDIA GPU 和 CUDA：

```powershell
pip install onnxruntime-gpu
```

修改 `main.py`:
```python
app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
```

### 自訂成員

修改 `main.py` 的 `members` 字典：

```python
members = {
    "member1": {"display": "成員1名稱", "korean": "한글"},
    "member2": {"display": "成員2名稱", "korean": "한글"},
    # ...
}
```

對應建立 `photos/member1/`, `photos/member2/` 資料夾。

## 授權與致謝

- **InsightFace**: Apache License 2.0
- **Gradio**: Apache License 2.0
- **TWICE 照片**: 僅供個人學習研究使用

## 疑難排解聯絡

如有問題，請檢查：
1. Python 版本: 3.9.x
2. 虛擬環境已啟動
3. 所有套件已正確安裝
4. 照片資料夾結構正確
5. 模型檔案已下載完整
