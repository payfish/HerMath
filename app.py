import streamlit as st
import requests

# 这是你的后端地址
API_URL = "http://127.0.0.1:8000"

# --- 页面配置 ---
st.set_page_config(page_title="Her Math", page_icon="❤️", layout="centered")

# CSS 美化 (为了让她看着舒服，把按钮变粉色，字体变大)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FFB6C1;
        color: white;
        border-radius: 20px;
        width: 100%;
    }
    .big-font {
        font-size:20px !important;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 标题区 ---
st.title("👸 笨笨数学本")
st.caption("专属你的数学私教：付鱼晏")

# --- 1. 获取知识点列表 ---
try:
    # 找后端要数据
    topics = requests.get(f"{API_URL}/topics/").json()
except:
    st.error("后端好像没启动？快去运行 uvicorn main:app")
    st.stop()

# --- 2. 侧边栏：选择课程 ---
# 提取所有课程的名字，让用户选
topic_names = [t['title'] for t in topics]
selected_topic_name = st.sidebar.selectbox("选择课程", topic_names)

# 找到当前选中的 topic_id
current_topic = next(t for t in topics if t['title'] == selected_topic_name)
topic_id = current_topic['id']

# --- 3. 显示“男友笔记” ---
st.header(f"📖 {selected_topic_name}")

# 获取笔记
response = requests.get(f"{API_URL}/topics/{topic_id}/notes")

if response.status_code == 200:
    notes = response.json()
    
    # 判断有没有笔记
    if notes and len(notes) > 0:
        st.caption(f"共 {len(notes)} 条爱心讲解") # 显示一下有多少条
        
        # === 关键修改：用循环把所有笔记都画出来 ===
        for note in notes:
            # 每一个笔记就是一个独立的蓝色气泡
            st.info(f"💡 {note['content']}")
            
    else:
        st.warning("博主还没写这一章的笔记哦~ (快去后台加一条！)")
else:
    st.error("无法获取笔记数据")

st.divider() # 分割线

# --- 4. 闯关做题 ---
st.subheader("📝 闯关练习")

# 获取题目
questions = requests.get(f"{API_URL}/topics/{topic_id}/questions").json()

if not questions:
    st.write("本章还没有题目，休息一下吧！")
else:
    # 遍历每一道题
    for i, q in enumerate(questions):
        st.markdown(f"<p class='big-font'><b>Q{i+1}:</b> {q['text']}</p>", unsafe_allow_html=True)
        
        # 处理选项 (把字符串 "A,B,C" 变成列表)
        options_list = q['options'].split(",")
        
        # 这是一个单选框，key必须唯一
        user_choice = st.radio(f"请选择 (第{i+1}题)", options_list, key=f"q_{q['id']}", horizontal=True)

        # 检查按钮
        if st.button(f"提交第 {i+1} 题", key=f"btn_{q['id']}"):
            if user_choice == q['correct_answer']:
                st.balloons() # 答对了大屏幕放气球！
                st.success("🎉 太棒了！亲亲你！")
            else:
                st.error("🤔 好像不对哦，看看提示？")
                with st.expander("点击查看男友的爱心提示"):
                    st.write(f"👉 {q['hint']}")
        
        st.markdown("---") # 题目之间的分割线