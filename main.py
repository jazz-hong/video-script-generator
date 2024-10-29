import streamlit as st
from utils import generate_script

st.title("🎬 视频脚本生成器")

with st.sidebar:
    api_key = st.text_input("请输入Chatgroq API密钥：", type="password")
    st.markdown("[获取Chatgroq API密钥](https://console.groq.com/keys)")

subject = st.text_input("💡 请输入视频的主题 Please enter the Subject of your Story")
video_length = st.number_input("⏱️ 请输入视频的大致时长（单位：分钟）Please enter the duration of Story (min)", min_value=0.1, step=0.1)
creativity = st.slider("✨ Creativity of Storyline (Temperature) 请输入视频脚本的创造力（数字小说明更严谨，数字大说明更多样）", min_value=0.0,
                       max_value=1.0, value=0.2, step=0.1)
submit = st.button("SUMBIT")

if submit and not api_key:
    st.info("Please Enter your ChatGroq API")
    st.stop()
if submit and not subject:
    st.info("Please enter the title of your Video")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("Video Duration must >= 0.1")
    st.stop()
if submit:
    with st.spinner("AI is now Thinking..."):
        search_result, title, script = generate_script(subject, video_length, creativity, api_key)
    st.success("视频脚本已生成！")
    st.subheader("🔥 TITLE 标题：")
    st.write(title)
    st.subheader("📝 SCRIPT 视频脚本：")
    st.write(script)
    with st.expander("WIKIPEDIA RESULT 维基百科搜索结果 👀"):
        st.info(search_result)
