import streamlit as st
import requests

# 后端地址
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="男友后台", page_icon="👨‍🏫")

st.title("👨‍🏫 瑶瑶专属私教控制台")
st.caption("在这里添加新的关卡和爱心笔记")

# --- 选项卡：把功能分开 ---
tab1, tab2, tab3 = st.tabs(["📚 加新课程", "💌 写笔记", "➕ 出题目"])

# === 功能 1：添加新课程 ===
with tab1:
    st.subheader("新建一个章节")
    new_title = st.text_input("章节标题 ")
    new_level = st.slider("难度等级", 1, 5, 1)
    
    if st.button("创建章节"):
        # 调用后端 API
        data = {"title": new_title, "level": new_level, "is_locked": False}
        res = requests.post(f"{API_URL}/topics/", json=data)
        if res.status_code == 200:
            st.success(f"成功创建：{new_title}！")
        else:
            st.error("创建失败")

# === 功能 2：给课程写笔记 ===
with tab2:
    st.subheader("✍️ 添加新笔记")
    
    # 1. 获取现有课程让用户选
    try:
        topics = requests.get(f"{API_URL}/topics/").json()
        if not topics:
            st.warning("还没有课程，先去Tab1建一个吧")
            st.stop()
            
        topic_dict = {t['title']: t['id'] for t in topics}
        selected_topic = st.selectbox("选择要写笔记的章节", list(topic_dict.keys()))
        selected_topic_id = topic_dict[selected_topic]
        
        # 2. 输入笔记内容
        note_content = st.text_area("输入你的爱心讲解 (支持 Markdown)", height=100, 
                                    placeholder="宝宝你看，这个问题其实很简单...")
        
        if st.button("发布笔记"):
            note_data = {
                "topic_id": selected_topic_id, 
                "content": note_content
            }
            res = requests.post(f"{API_URL}/notes/", json=note_data)
            if res.status_code == 200:
                st.success("笔记已发布！")
                st.rerun() # 发布完自动刷新页面，让你立刻看到下面的列表更新
            else:
                st.error("发布失败")

        st.divider() # 分割线
        
        # 3. === 新增功能：管理/删除已有笔记 ===
        st.subheader(f"🗑️ 管理已发布的笔记 ({selected_topic})")
        
        # 获取该章节下的所有笔记
        notes_res = requests.get(f"{API_URL}/topics/{selected_topic_id}/notes")
        
        if notes_res.status_code == 200:
            notes = notes_res.json()
            if notes:
                # 遍历所有笔记，一行一个
                for note in notes:
                    # 使用列布局：左边显示内容，右边放个小小的删除按钮
                    col1, col2 = st.columns([5, 1]) 
                    
                    with col1:
                        st.info(note['content']) # 显示笔记内容
                        
                    with col2:
                        # 这是一个红色按钮，key必须唯一（用笔记ID做key）
                        if st.button("删除", key=f"del_{note['id']}", type="primary"):
                            # 调用刚才写的后端删除接口
                            del_res = requests.delete(f"{API_URL}/notes/{note['id']}")
                            if del_res.status_code == 200:
                                st.success("已删除")
                                st.rerun() # 删除成功后立马刷新页面，让它消失
            else:
                st.caption("该章节下暂无笔记")
                
    except Exception as e:
        st.error(f"连接后端失败: {e}")

# === 功能 3：出题 ===
with tab3:
    st.subheader("添加闯关题目")
    
    if 'topic_dict' in locals():
        q_topic = st.selectbox("出题给哪个章节？", list(topic_dict.keys()), key="q_topic")
        
        q_text = st.text_input("题目描述", "1+1等于几？")
        q_options = st.text_input("选项 (用英文逗号隔开)", "1,2,3,4")
        q_answer = st.text_input("正确答案", "2")
        q_hint = st.text_input("爱心提示 (Hint)", "伸出手指头数一数...")
        
        if st.button("提交题目"):
            q_data = {
                "topic_id": topic_dict[q_topic],
                "text": q_text,
                "options": q_options,
                "correct_answer": q_answer,
                "hint": q_hint
            }
            res = requests.post(f"{API_URL}/questions/", json=q_data)
            if res.status_code == 200:
                st.success("题目添加成功！")
            else:
                st.error("出题失败")