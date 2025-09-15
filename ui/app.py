import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import uuid
import pandas as pd
import streamlit as st
import retrieval.response
import retrieval.query_rewrite
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime


if 'chat_blocks' not in st.session_state:
    st.session_state.chat_blocks= []

if 'dashboard_blocks' not in st.session_state:
    st.session_state.dashboard_blocks = []

def get_information(input_text, modified_query, response, start, end):

    original_query = input_text
    rewrite_query = modified_query.text
    
    input_token = modified_query.usage_metadata.prompt_token_count
    ouput_token = modified_query.usage_metadata.candidates_token_count

    ouput_response_token = response.usage_metadata.candidates_token_count

    dashboard_block = {
        'original_query': original_query,
        'modified_query': rewrite_query,
        'input_tokens': input_token,
        'output_tokens': ouput_response_token,
        'extra_tokens': ouput_token * 2,
        'time': end-start,
        'timestamp': datetime.now(),
        'total_tokens': input_token + ouput_response_token + (ouput_token * 2),
        'query_modified': original_query.strip().lower() != rewrite_query.strip().lower()
    }

    return dashboard_block

def load_chats():

    for index, block in enumerate(st.session_state.chat_blocks):

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

        if block['output']:

            sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]

            feedback_value = (
                'Negative' if block.get('feedback') == sentiment_mapping[0] else
                'Positive' if block.get('feedback') == sentiment_mapping[1] else
                None
            )

            selected = st.feedback(
                "thumbs",
                key=f'feedback_{index}',
            )

            if selected is not None and selected != feedback_value:
                st.markdown(f"You selected: {sentiment_mapping[selected]}")
                block['feedback'] = sentiment_mapping[selected]

                if index < len(st.session_state.dashboard_blocks):
                    st.session_state.dashboard_blocks[index]['feedback'] = feedback_value


        st.markdown("<br>", unsafe_allow_html=True)

def render_chat_page():

    st.markdown("<h2 style = 'text-align: center;'>Director's Cut 1.0</h2>",
            unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    load_chats()

    user_input = st.chat_input("your query here", key=f'chat_input_{len(st.session_state.chat_blocks)}')

    if user_input:

        start_time = time.time()

        st.session_state.user_interacted = True

        chat_block = {'text': "", 'output': ""}
        chat_block['text'] = user_input

        modified_query = retrieval.query_rewrite.rewrite_query(text_input=chat_block['text'])
        response = retrieval.response.get_response(question=modified_query.text)
        chat_block['output'] = response.text

        end_time = time.time()

        st.session_state.chat_blocks.append(chat_block)
        st.session_state.dashboard_blocks.append(get_information(chat_block['text'], modified_query, response, start_time, end_time))
        st.rerun()


def render_dashboard_page():

    st.markdown("<h2 style='text-align: center;'>Analytics Dashboard</h2>", unsafe_allow_html=True)
    
    if not st.session_state.dashboard_blocks:
        st.info("🔍 No analytics data available yet. Start chatting to see insights!")
        st.markdown("---")
        st.markdown("### What you'll see here once you start chatting:")
        st.markdown("- **Performance Metrics**: Response times, token usage, efficiency trends")
        st.markdown("- **Query Analysis**: How often queries are rewritten and modified")
        st.markdown("- **Token Economics**: Input, output, and processing token breakdowns")
        st.markdown("- **User Feedback**: Satisfaction rates and feedback trends")
        return

    df = pd.DataFrame(st.session_state.dashboard_blocks)
    
    st.subheader("📈 Overview Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_chats = len(df)
        st.metric(
            label="Total Conversations",
            value=f"{total_chats:,}",
            help="Total number of chat interactions"
        )
    
    with col2:
        avg_time = df['time'].mean()
        st.metric(
            label="Avg Response Time",
            value=f"{avg_time:.2f}s",
            help="Average time to generate responses"
        )
    
    with col3:
        total_tokens = df['total_tokens'].sum()
        st.metric(
            label="Total Tokens Used",
            value=f"{total_tokens:,}",
            help="Sum of all input, output, and processing tokens"
        )
    
    with col4:
        if 'feedback' in df.columns and df['feedback'].notna().any():
            positive_feedback = len(df[df['feedback'] == 'Positive'])
            total_feedback = len(df[df['feedback'].notna()])
            satisfaction_rate = (positive_feedback / total_feedback * 100) if total_feedback > 0 else 0
            st.metric(
                label="Satisfaction Rate",
                value=f"{satisfaction_rate:.1f}%",
                help="Percentage of positive feedback"
            )
        else:
            avg_tokens_per_chat = df['total_tokens'].mean()
            st.metric(
                label="Avg Tokens/Chat",
                value=f"{avg_tokens_per_chat:.0f}",
                help="Average"
            )

    st.divider()
    
    st.subheader("⚡ Performance Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_time = px.line(
            df.reset_index(),
            x='index',
            y='time',
            title="Response Time Trend",
            labels={'index': 'Chat Number', 'time': 'Response Time (seconds)'},
            line_shape='spline'
        )
        fig_time.update_traces(line_color='#00D4AA', line_width=3)
        fig_time.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        fig_tokens = go.Figure()
        
        fig_tokens.add_trace(go.Scatter(
            x=list(range(len(df))),
            y=df['input_tokens'],
            mode='lines+markers',
            name='Input Tokens',
            line=dict(color='#FF6B6B', width=2),
            fill='tonexty'
        ))
        
        fig_tokens.add_trace(go.Scatter(
            x=list(range(len(df))),
            y=df['output_tokens'],
            mode='lines+markers',
            name='Output Tokens',
            line=dict(color='#4ECDC4', width=2),
            fill='tonexty'
        ))
        
        fig_tokens.add_trace(go.Scatter(
            x=list(range(len(df))),
            y=df['extra_tokens'],
            mode='lines+markers',
            name='Processing Tokens',
            line=dict(color='#45B7D1', width=2),
            fill='tonexty'
        ))
        
        fig_tokens.update_layout(
            title="Token Usage Over Time",
            xaxis_title="Chat Number",
            yaxis_title="Token Count",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_tokens, use_container_width=True)
    
    st.subheader("💰 Token Economics")
    col1, col2 = st.columns(2)
    
    with col1:
        total_input = df['input_tokens'].sum()
        total_output = df['output_tokens'].sum()
        total_extra = df['extra_tokens'].sum()
        
        fig_pie = px.pie(
            values=[total_input, total_output, total_extra],
            names=['Input Tokens', 'Output Tokens', 'Processing Tokens'],
            title="Token Usage Distribution",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
        )
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        df['efficiency'] = df['output_tokens'] / df['total_tokens']
        fig_efficiency = px.bar(
            df.reset_index().tail(10),
            x='index',
            y='efficiency',
            title="Recent Token Efficiency (Output/Total)",
            labels={'index': 'Recent Chats', 'efficiency': 'Efficiency Ratio'},
            color='efficiency',
            color_continuous_scale='Viridis'
        )
        fig_efficiency.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_efficiency, use_container_width=True)
    
    st.subheader("🔄 Query Analysis")
    
    modified_count = df['query_modified'].sum()
    total_queries = len(df)
    modification_rate = (modified_count / total_queries * 100) if total_queries > 0 else 0
    
    fig_modification = px.pie(
        values=[modified_count, total_queries - modified_count],
        names=[f'Modified ({modification_rate:.1f}%)', f'Original ({100-modification_rate:.1f}%)'],
        title="Query Modification Rate",
        color_discrete_sequence=['#FF9F43', '#6C5CE7']
    )
    fig_modification.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig_modification, use_container_width=True)
    
    if 'feedback' in df.columns and df['feedback'].notna().any():
        st.subheader("👍 User Feedback Analysis")
        
        feedback_df = df[df['feedback'].notna()]
        
        feedback_counts = feedback_df['feedback'].value_counts()
        fig_feedback = px.bar(
            x=feedback_counts.index,
            y=feedback_counts.values,
            title="Feedback Distribution",
            color=feedback_counts.values,
            color_continuous_scale='RdYlGn'
        )
        fig_feedback.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_feedback, use_container_width=True)
        
def main():

    st.set_page_config(
        page_title='Directors-Cut-1.0',
        layout='centered',
        initial_sidebar_state='expanded'
    )

    with st.sidebar:
        st.title('Navigation')

        page = st.radio(
            "Choose a page:",
            ['Chat', 'Dashboard']
        )

    if page == 'Chat':
        render_chat_page()
    if page == 'Dashboard':
        render_dashboard_page()

if __name__ == '__main__':
    main()