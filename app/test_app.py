import streamlit as st
import PyPDF2

st.title("Test App")
st.write("PyPDF2 is working!")

try:
    st.success(f"PyPDF2 version: {PyPDF2.__version__}")
except:
    st.error("PyPDF2 not found")