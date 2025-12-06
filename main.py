# 🎤 TWICE 成員人臉辨識教學程式

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import glob
import random
from PIL import Image
import insightface
from insightface.app import FaceAnalysis

# ==================== 成員設定 ====================

# 成員英文名 (用於資料夾名稱)
members_en = "ny,jy,mo,sa,jh,mi,dh,cy,ty"

# 成員中文名 (用於顯示)
members_zh = "娜璉나연,定延정연,momo모모,sana사나,志效지효,mina미나,多賢다현,彩瑛채영,子瑜쯔위"

# 將字串轉換為列表，方便後續使用
members_en_list = members_en.split(',')
members_zh_list = members_zh.split(',')

# 建立成員對應字典
member_dict = dict(zip(members_en_list, members_zh_list))

print("🎉 TWICE 成員設定完成！")
print("="*50)
for en_name, zh_name in member_dict.items():
    print(f"📁 資料夾名稱: {en_name} → 顯示名稱: {zh_name}")
print("="*50)

# ==================== 環境設定 ====================

print("📚 套件導入完成！")

# 設定中文字體顯示 (for matplotlib)
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

print("✅ 環境設定完成！準備開始人臉辨識...")

# ==================== 建立人臉辨識模型 ====================

# 初始化 InsightFace 模型
print("🚀 正在載入 InsightFace 模型...")
app = FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))
app.det_model.det_thresh = 0.4  # 將預設的 0.5 降到 0.3
print("✅ 模型載入完成！")

# 建立人臉特徵資料庫
face_database = {}
member_names = []

def extract_face_features(image_path):
    """提取人臉特徵"""
    img = cv2.imread(image_path)
    if img is None:
        return None

    faces = app.get(img)
    if len(faces) == 0:
        return None

    # 取第一張臉的特徵
    return faces[0].embedding

# ==================== 建立訓練資料庫 ====================

# 從 photos 資料夾建立人臉特徵資料庫
print("📸 正在建立人臉特徵資料庫...")
for member_en in members_en_list:
    member_zh = member_dict[member_en]
    photo_dir = os.path.join('photos', member_en)

    if not os.path.exists(photo_dir):
        print(f"⚠️  警告: {photo_dir} 資料夾不存在或無照片")
        continue

    # 獲取該成員所有照片
    image_files = glob.glob(os.path.join(photo_dir, '*'))
    image_files = [f for f in image_files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

    if len(image_files) == 0:
        print(f"⚠️  警告: {member_zh} 的資料夾中沒有找到照片")
        continue

    member_features = []
    successful_images = 0

    for img_path in image_files:
        features = extract_face_features(img_path)
        if features is not None:
            member_features.append(features)
            successful_images += 1

    if len(member_features) > 0:
        # 計算平均特徵向量
        avg_features = np.mean(member_features, axis=0)
        face_database[member_en] = avg_features
        member_names.append(member_en)
        print(f"✅ {member_zh}: 成功處理 {successful_images}/{len(image_files)} 張照片")
    else:
        print(f"❌ {member_zh}: 無法從照片中提取人臉特徵")

print(f"\n🎉 人臉特徵資料庫建立完成！成功建立 {len(face_database)} 位成員的特徵資料")
print("資料庫包含的成員:", [member_dict[name] for name in member_names])

# ==================== 人臉辨識功能 ====================

def recognize_face(image_path, threshold=0.6):
    """辨識人臉"""
    features = extract_face_features(image_path)
    if features is None:
        return None, 0

    best_match = None
    best_score = float('inf')

    for member_en, db_features in face_database.items():
        # 計算餘弦相似度
        similarity = np.dot(features, db_features) / (np.linalg.norm(features) * np.linalg.norm(db_features))
        distance = 1 - similarity

        if distance < best_score:
            best_score = distance
            best_match = member_en

    confidence = 1 - best_score
    if confidence < threshold:
        return None, confidence

    return best_match, confidence

def display_test_results():
    """顯示測試結果"""
    test_results = []

    print("🔍 正在測試 test_photos 中的照片...")
    print("="*80)

    for member_en in members_en_list:
        member_zh = member_dict[member_en]
        test_dir = os.path.join('test_photos', member_en)

        if not os.path.exists(test_dir):
            continue

        image_files = glob.glob(os.path.join(test_dir, '*'))
        image_files = [f for f in image_files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

        if len(image_files) == 0:
            continue

        for img_path in image_files:
            predicted_member, confidence = recognize_face(img_path)

            if predicted_member:
                predicted_zh = member_dict[predicted_member]
                is_correct = predicted_member == member_en
                status = "✅ 正確" if is_correct else "❌ 錯誤"

                print(f"📷 {os.path.basename(img_path)}")
                print(f"   實際: {member_zh}")
                print(f"   預測: {predicted_zh} (信心度: {confidence:.2f})")
                print(f"   結果: {status}")

                test_results.append({
                    'image': os.path.basename(img_path),
                    'actual': member_zh,
                    'predicted': predicted_zh,
                    'confidence': confidence,
                    'correct': is_correct
                })
            else:
                print(f"📷 {os.path.basename(img_path)}")
                print(f"   實際: {member_zh}")
                print(f"   預測: 無法辨識 (信心度過低)")
                print(f"   結果: ❌ 無法辨識")

                test_results.append({
                    'image': os.path.basename(img_path),
                    'actual': member_zh,
                    'predicted': "無法辨識",
                    'confidence': confidence if predicted_member else 0,
                    'correct': False
                })

            print("-" * 50)

    # 統計結果
    if test_results:
        correct_count = sum(1 for result in test_results if result['correct'])
        total_count = len(test_results)
        accuracy = correct_count / total_count * 100

        print(f"\n📊 測試結果統計:")
        print(f"總測試張數: {total_count}")
        print(f"正確辨識: {correct_count}")
        print(f"準確率: {accuracy:.1f}%")

        return test_results
    else:
        print("⚠️  test_photos 資料夾中沒有找到測試照片")
        return []

# 執行測試
test_results = display_test_results()

print("\n" + "="*50)
print("✅ 人臉特徵資料庫建立完成！")
print(f"📊 準確率: {sum(1 for r in test_results if r['correct']) / len(test_results) * 100:.1f}%" if test_results else "無測試資料")
print("="*50)
