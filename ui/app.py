import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import retrieval.response
import retrieval.query_rewrite


st.markdown("<h2 style = 'text-align: center;'>Director's Cut 1.0</h2>",
            unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

if 'blocks' not in st.session_state:
    st.session_state.blocks = [{
                                'text': "", 
                                'output': ""
                                }]

if 'user_interacted' not in st.session_state:
    st.session_state.user_interacted = False

for index, block in enumerate(st.session_state.blocks):

    left, right = st.columns([0.6, 0.4])

    with right:
        st.markdown(
            f"""
            <div style="
                background-color: rgba(0, 123, 255, 0.15);
                padding: 10px 15px;
                border-radius: 10px;
                margin-bottom: 10px;
                text-align: left;
                max-width: 90%;
                float: right;
                clear: both;
                font-size: 18px;
                color: inherit;
                opacity: 0.8
            ">
                {block['text']}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div style="
            background-color: rgba(255, 255, 255, 0.07);
            padding: 10px 15px;
            border-radius: 10px;
            margin-top: 5px;
            max-width: 90%;
            float: left;
            clear: both;
            font-size: 17px;
            color: inherit;
            opacity: 0.8
        ">
            {block['output']}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)


user_input = st.chat_input("your query here")

if user_input:
    st.session_state.user_interacted = True
    curr_block = {'text': "", 'output': ""}
    curr_block['text'] = user_input
    modified_query = retrieval.query_rewrite.rewrite_query(text_input=curr_block['text'])
    curr_block['output'] = retrieval.response.get_response(question=modified_query)
    st.session_state.blocks.append(curr_block)

if st.session_state.user_interacted:
    st.session_state.user_interacted = False
    st.rerun()

