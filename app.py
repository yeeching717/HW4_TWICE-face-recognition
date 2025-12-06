# 🎤 TWICE 成員辨識 PK 大賽 - Streamlit 介面

import os
import glob
import random
import streamlit as st
from PIL import Image

# 導入 main.py 的功能
from main import (
    members_en_list,
    member_dict,
    recognize_face
)

# ==================== Streamlit 互動 PK 遊戲 ====================

def initialize_game():
    """初始化遊戲，收集所有測試照片"""
    test_images = []

    for member_en in members_en_list:
        test_dir = os.path.join('test_photos', member_en)
        if os.path.exists(test_dir):
            image_files = glob.glob(os.path.join(test_dir, '*'))
            image_files = [f for f in image_files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

            for img_path in image_files:
                test_images.append({
                    'path': img_path,
                    'answer': member_en,
                    'answer_zh': member_dict[member_en]
                })

    random.shuffle(test_images)
    return test_images

# ==================== Streamlit 介面 ====================

def main():
    """Streamlit 主程式"""
    st.set_page_config(
        page_title="TWICE 成員辨識 PK 大賽",
        page_icon="🎤",
        layout="wide"
    )

    # 初始化 session state
    if 'test_images' not in st.session_state:
        st.session_state.test_images = initialize_game()
        st.session_state.current_index = 0
        st.session_state.user_score = 0
        st.session_state.ai_score = 0
        st.session_state.round_count = 0
        st.session_state.game_started = False
        st.session_state.answered = False
        st.session_state.ai_prediction = None
        st.session_state.ai_confidence = 0

    # 標題
    st.markdown("""
    <div style="text-align: center;">
        <h1>🎤 TWICE 成員辨識 PK 大賽 🎤</h1>
        <p>和 AI 一起來辨識 TWICE 成員吧！看看誰比較厲害？</p>
    </div>
    """, unsafe_allow_html=True)

    # 分數顯示
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.metric("👤 玩家分數", st.session_state.user_score)
    with col2:
        st.metric("🎮 回合數", st.session_state.round_count)
    with col3:
        st.metric("🤖 AI分數", st.session_state.ai_score)

    st.divider()

    # 遊戲區域
    if not st.session_state.game_started:
        st.info(f"📸 已找到 {len(st.session_state.test_images)} 張測試照片")
        if st.button("🎯 開始遊戲", type="primary", use_container_width=True):
            st.session_state.game_started = True
            st.session_state.current_index = 0
            st.rerun()
    else:
        # 檢查是否還有題目
        if st.session_state.current_index >= len(st.session_state.test_images):
            st.success("🎉 遊戲結束！")
            st.markdown(f"""
            ### 📊 最終結果
            - 👤 玩家得分: **{st.session_state.user_score}**
            - 🤖 AI得分: **{st.session_state.ai_score}**
            """)
            
            if st.session_state.user_score > st.session_state.ai_score:
                st.balloons()
                st.success("🏆 恭喜你獲勝！")
            elif st.session_state.user_score < st.session_state.ai_score:
                st.error("🤖 AI獲勝！繼續加油！")
            else:
                st.info("🤝 平手！實力相當！")

            if st.button("🔄 重新開始", type="primary", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        else:
            # 顯示當前題目
            current_img_data = st.session_state.test_images[st.session_state.current_index]
            
            col_left, col_right = st.columns([1, 1])
            
            with col_left:
                st.subheader("🖼️ 猜猜這是哪位成員？")
                img = Image.open(current_img_data['path'])
                st.image(img, use_container_width=True)
                
                # AI 預測資訊
                if st.session_state.ai_prediction:
                    st.info(f"🧠 AI預測: {member_dict.get(st.session_state.ai_prediction, '無法辨識')} (信心度: {st.session_state.ai_confidence:.2f})")

            with col_right:
                st.subheader("👤 選擇你的答案")
                
                user_choice = st.radio(
                    "TWICE 成員",
                    options=[member_dict[member] for member in members_en_list],
                    key=f"choice_{st.session_state.current_index}",
                    disabled=st.session_state.answered
                )

                # 提交答案按鈕
                if not st.session_state.answered:
                    if st.button("✅ 提交答案", type="primary", use_container_width=True):
                        # AI 進行預測
                        ai_pred, ai_conf = recognize_face(current_img_data['path'])
                        st.session_state.ai_prediction = ai_pred
                        st.session_state.ai_confidence = ai_conf
                        
                        # 檢查答案
                        correct_answer = current_img_data['answer']
                        correct_answer_zh = current_img_data['answer_zh']
                        
                        # 將選擇的中文名稱轉回英文代碼
                        user_choice_en = None
                        for en, zh in member_dict.items():
                            if zh == user_choice:
                                user_choice_en = en
                                break
                        
                        user_correct = (user_choice_en == correct_answer)
                        ai_correct = (ai_pred == correct_answer)
                        
                        if user_correct:
                            st.session_state.user_score += 1
                        if ai_correct:
                            st.session_state.ai_score += 1
                        
                        st.session_state.round_count += 1
                        st.session_state.answered = True
                        st.rerun()
                
                # 顯示結果
                if st.session_state.answered:
                    correct_answer = current_img_data['answer']
                    correct_answer_zh = current_img_data['answer_zh']
                    
                    # 將選擇的中文名稱轉回英文代碼
                    user_choice_en = None
                    for en, zh in member_dict.items():
                        if zh == user_choice:
                            user_choice_en = en
                            break
                    
                    user_correct = (user_choice_en == correct_answer)
                    ai_correct = (st.session_state.ai_prediction == correct_answer)
                    
                    st.markdown("---")
                    st.subheader("📝 本回合結果")
                    st.markdown(f"**🎯 正確答案:** {correct_answer_zh}")
                    st.markdown(f"**👤 你的答案:** {user_choice} {'✅' if user_correct else '❌'}")
                    st.markdown(f"**🤖 AI的答案:** {member_dict.get(st.session_state.ai_prediction, '無法辨識')} {'✅' if ai_correct else '❌'}")
                    
                    # 下一題按鈕
                    if st.button("➡️ 下一題", type="primary", use_container_width=True):
                        st.session_state.current_index += 1
                        st.session_state.answered = False
                        st.session_state.ai_prediction = None
                        st.session_state.ai_confidence = 0
                        st.rerun()

    # 側邊欄 - 重置遊戲
    with st.sidebar:
        st.header("🎮 遊戲選項")
        if st.button("🔄 重新開始遊戲", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.divider()
        st.markdown("### 📊 統計資訊")
        st.markdown(f"總題數: {len(st.session_state.test_images) if 'test_images' in st.session_state else 0}")
        st.markdown(f"已完成: {st.session_state.round_count if 'round_count' in st.session_state else 0}")

if __name__ == "__main__":
    main()
