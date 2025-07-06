#!/usr/bin/env python3
"""
企业文档检索 RAG 系统 - 简化界面
直接使用 Knowledge Base API
"""

import streamlit as st
import boto3
import time
import logging
from datetime import datetime

# 配置页面
st.set_page_config(
    page_title="企业文档检索系统",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .info-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    .citation {
        font-size: 0.8rem;
        color: #666;
        background-color: #f5f5f5;
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 知识库配置
KNOWLEDGE_BASE_ID = "HCDVL6Q0KZ"
MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0"

# 初始化会话状态
def initialize_session():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'bedrock_client' not in st.session_state:
        st.session_state.bedrock_client = boto3.client('bedrock-agent-runtime')

def query_knowledge_base(question):
    """查询知识库"""
    try:
        response = st.session_state.bedrock_client.retrieve_and_generate(
            input={'text': question},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KNOWLEDGE_BASE_ID,
                    'modelArn': MODEL_ARN
                }
            }
        )
        
        answer = response['output']['text']
        citations = []
        
        # 提取引用来源
        for citation in response.get('citations', []):
            for ref in citation.get('retrievedReferences', []):
                source = ref.get('location', {}).get('s3Location', {}).get('uri', '')
                if source:
                    # 提取文件名
                    filename = source.split('/')[-1]
                    citations.append(filename)
        
        return answer, citations
        
    except Exception as e:
        st.error(f"查询失败: {str(e)}")
        return None, []

def main():
    # 初始化
    initialize_session()
    
    # 页面标题
    st.markdown('<h1 class="main-header">🏢 企业文档检索系统</h1>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.header("📋 系统信息")
        
        # 系统状态
        st.markdown('<div class="success-box">✅ 系统运行正常</div>', unsafe_allow_html=True)
        st.write(f"**知识库 ID**: {KNOWLEDGE_BASE_ID}")
        st.write(f"**当前时间**: {datetime.now().strftime('%H:%M:%S')}")
        st.write(f"**对话轮次**: {len(st.session_state.chat_history)}")
        
        st.divider()
        
        # 快速查询示例
        st.subheader("💡 查询示例")
        example_queries = [
            "公司的请假制度是什么？",
            "如何申请年假？",
            "网络连接问题怎么解决？",
            "差旅费报销标准是多少？",
            "VPN怎么设置？",
            "加班工资如何计算？",
            "如何申请设备采购？",
            "财务审批流程是什么？"
        ]
        
        for query in example_queries:
            if st.button(query, key=f"example_{hash(query)}", use_container_width=True):
                st.session_state.current_query = query
                
        st.divider()
        
        # 系统管理
        st.subheader("⚙️ 系统管理")
        
        if st.button("🔄 刷新页面", use_container_width=True):
            st.rerun()
            
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
            
        # 文档类型说明
        st.divider()
        st.subheader("📚 支持的文档")
        doc_types = [
            "📋 公司政策制度",
            "🛠️ IT支持文档", 
            "💰 财务管理制度"
        ]
        
        for doc_type in doc_types:
            st.write(doc_type)
    
    # 主界面
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 系统介绍
        if not st.session_state.chat_history:
            st.markdown("""
            ### 👋 欢迎使用企业文档检索系统
            
            这是一个基于 **Amazon Bedrock Knowledge Base** 的智能文档检索系统，可以帮助您：
            
            - 🔍 **快速检索**：在企业文档中快速找到所需信息
            - 📋 **政策查询**：查询公司政策、制度和规定
            - 🛠️ **技术支持**：获取IT支持和技术文档
            - 💰 **财务信息**：了解财务制度和报销流程
            
            **使用方法**：在下方输入框中输入您的问题，系统会自动检索相关文档并提供答案。
            """)
            
            st.markdown('<div class="info-box">💡 提示：您可以使用侧边栏的示例查询快速开始，或者直接输入您的问题</div>', unsafe_allow_html=True)
        
        # 聊天历史
        for i, (question, answer, citations) in enumerate(st.session_state.chat_history):
            st.markdown(f'<div class="chat-message user-message"><strong>🙋 您：</strong> {question}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-message assistant-message"><strong>🤖 助手：</strong> {answer}</div>', unsafe_allow_html=True)
            
            # 显示引用来源
            if citations:
                citations_text = "📚 **信息来源**: " + ", ".join(set(citations))
                st.markdown(f'<div class="citation">{citations_text}</div>', unsafe_allow_html=True)
        
        # 查询输入
        # 检查是否有预设查询
        default_query = st.session_state.get('current_query', '')
        if default_query:
            st.session_state.current_query = ''  # 清除预设查询
            
        query = st.chat_input("请输入您的问题...") or default_query
        
        if query:
            with st.spinner("🔍 正在检索文档..."):
                # 显示用户问题
                st.markdown(f'<div class="chat-message user-message"><strong>🙋 您：</strong> {query}</div>', unsafe_allow_html=True)
                
                # 查询知识库
                start_time = time.time()
                answer, citations = query_knowledge_base(query)
                end_time = time.time()
                
                if answer:
                    # 显示结果
                    st.markdown(f'<div class="chat-message assistant-message"><strong>🤖 助手：</strong> {answer}</div>', unsafe_allow_html=True)
                    
                    # 显示引用来源
                    if citations:
                        citations_text = "📚 **信息来源**: " + ", ".join(set(citations))
                        st.markdown(f'<div class="citation">{citations_text}</div>', unsafe_allow_html=True)
                    
                    # 添加到历史记录
                    st.session_state.chat_history.append((query, answer, citations))
                    
                    # 显示查询时间
                    st.caption(f"⏱️ 查询耗时: {end_time - start_time:.2f} 秒")
    
    with col2:
        # 实时统计
        st.subheader("📊 实时统计")
        
        if st.session_state.chat_history:
            total_queries = len(st.session_state.chat_history)
            avg_response_length = sum(len(item[1]) for item in st.session_state.chat_history) / total_queries
            
            st.metric("总查询次数", total_queries)
            st.metric("平均回答长度", f"{avg_response_length:.0f} 字符")
        else:
            st.write("暂无查询记录")
            
        st.divider()
        
        # 使用提示
        st.subheader("💡 使用提示")
        tips = [
            "尽量使用具体的关键词",
            "可以询问具体的政策条款",
            "支持中文自然语言查询",
            "可以要求提供操作步骤",
            "系统会显示信息来源"
        ]
        
        for tip in tips:
            st.write(f"• {tip}")
            
        st.divider()
        
        # 技术信息
        st.subheader("🔧 技术架构")
        st.write("**模型**: Amazon Nova Pro")
        st.write("**向量化**: Titan Embed v2")
        st.write("**存储**: OpenSearch Serverless")
        st.write("**文档**: S3 + Knowledge Base")

if __name__ == "__main__":
    main()
