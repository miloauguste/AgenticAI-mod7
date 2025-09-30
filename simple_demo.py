"""
Simple demo without complex dependencies
"""
import streamlit as st

st.title("🚀 Content Creation System")
st.write("Multi-Agent Content Generator")

topic = st.text_input("Enter topic:", "AI automation")
content_type = st.selectbox("Content type:", ["blog_post", "social_media"])

if st.button("Generate"):
    st.write(f"Generating {content_type} about {topic}...")
    st.success("Demo complete! Install full requirements for complete functionality.")