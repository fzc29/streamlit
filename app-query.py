import streamlit as st
from trash.query_rag import multi_stage_query

st.set_page_config(page_title="Portfolio AI", page_icon="📊", layout="wide")

st.title("📊 Portfolio Newsletter Generator")

st.markdown(
    "Generate portfolio commentary using internal research databases."
)

query = st.text_area(
    "Enter Request",
    height=160,
    placeholder="Example: Draft a weekly performance summary..."
)

generate = st.button("Generate")

if generate and query.strip():

    with st.spinner("Running analysis..."):

        response, docs = multi_stage_query(query)

    st.divider()

    st.subheader("Generated Output")
    st.markdown(response.content)

    with st.expander("View Retrieved Sources"):
        for i, doc in enumerate(docs):
            st.markdown(f"**Source {i+1}**")
            st.write(doc.page_content[:1000])
            st.divider()

elif generate:
    st.warning("Please enter a request.")
