import sys
import os

import streamlit as st
import hybrid.response

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


st.markdown("<h2 style = 'text-align: center;'>Director's Cut 1.0</h2>",
            unsafe_allow_html=True)

st.markdown("<h4 style = 'text-align: center;'>What's in your mind?</h4>",
            unsafe_allow_html=True)


if 'blocks' not in st.session_state:
    st.session_state.blocks = [{
                                'text': "", 
                                'output': ""
                                }]

if 'user_interacted' not in st.session_state:
    st.session_state.user_interacted = False

for index, block in enumerate(st.session_state.blocks):

    user_input = st.text_input("", key=f'text_{index}')
    block['text'] = user_input

    if st.button('find', key=f'button_{index}'):

        if not block['text']:
            block['output'] = "Please add a query..."
        else:
            block['output'] = hybrid.response.get_response(question=block['text'])
            st.session_state.user_interacted = True
        
    st.write(block['output'])

if st.session_state.user_interacted:
    st.session_state.blocks.append({'text': "", 'output': ""})
    st.session_state.user_interacted = False
    st.rerun()

