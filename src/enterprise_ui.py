#!/usr/bin/env python3
"""
企业文档检索 RAG 系统 - Streamlit 界面
"""

import streamlit as st
import sys
import os
import time
import logging
from datetime import datetime

# 添加路径
sys.path.append('/home/ec2-user/amazon-bedrock-agent-workshop-for-gcr')
from src.utils.bedrock_agent import agents_helper
from enterprise_rag import EnterpriseRAG

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
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
def initialize_session():
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = EnterpriseRAG()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'agent_ready' not in st.session_state:
        st.session_state.agent_ready = False
        
    if 'system_info' not in st.session_state:
        st.session_state.system_info = {}

def check_agent_status():
    """检查Agent状态"""
    try:
        agent_id = agents_helper.get_agent_id_by_name("enterprise_document_assistant")
        agent_alias_id = agents_helper.get_agent_latest_alias_id(agent_id)
        
        st.session_state.rag_system.agent_id = agent_id
        st.session_state.rag_system.agent_alias_id = agent_alias_id
        st.session_state.agent_ready = True
        st.session_state.system_info = {
            'agent_id': agent_id,
            'agent_alias_id': agent_alias_id,
            'status': '运行中'
        }
        return True
    except:
        st.session_state.agent_ready = False
        st.session_state.system_info = {'status': '未部署'}
        return False

def main():
    # 初始化
    initialize_session()
    
    # 页面标题
    st.markdown('<h1 class="main-header">🏢 企业文档检索系统</h1>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.header("📋 系统控制")
        
        # 系统状态
        st.subheader("🔍 系统状态")
        if check_agent_status():
            st.markdown('<div class="success-box">✅ 系统运行正常</div>', unsafe_allow_html=True)
            st.write(f"**Agent ID**: {st.session_state.system_info.get('agent_id', 'N/A')[:10]}...")
        else:
            st.markdown('<div class="info-box">⚠️ 系统未部署</div>', unsafe_allow_html=True)
            
        st.divider()
        
        # 快速查询示例
        st.subheader("💡 查询示例")
        example_queries = [
            "公司的请假制度是什么？",
            "如何申请年假？",
            "网络连接问题怎么解决？",
            "差旅费报销标准是多少？",
            "VPN怎么设置？",
            "加班工资如何计算？"
        ]
        
        for query in example_queries:
            if st.button(query, key=f"example_{hash(query)}", use_container_width=True):
                st.session_state.current_query = query
                
        st.divider()
        
        # 系统管理
        st.subheader("⚙️ 系统管理")
        
        if st.button("🔄 刷新状态", use_container_width=True):
            st.rerun()
            
        if st.button("📊 查看日志", use_container_width=True):
            st.session_state.show_logs = True
            
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # 主界面
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 系统介绍
        if not st.session_state.chat_history:
            st.markdown("""
            ### 👋 欢迎使用企业文档检索系统
            
            这是一个基于 Amazon Bedrock 的智能文档检索系统，可以帮助您：
            
            - 🔍 **快速检索**：在企业文档中快速找到所需信息
            - 📋 **政策查询**：查询公司政策、制度和规定
            - 🛠️ **技术支持**：获取IT支持和技术文档
            - 💰 **财务信息**：了解财务制度和报销流程
            
            **使用方法**：在下方输入框中输入您的问题，系统会自动检索相关文档并提供答案。
            """)
            
            st.markdown('<div class="info-box">💡 提示：您可以使用侧边栏的示例查询快速开始</div>', unsafe_allow_html=True)
        
        # 聊天历史
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            st.markdown(f'<div class="chat-message user-message"><strong>🙋 您：</strong> {question}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-message assistant-message"><strong>🤖 助手：</strong> {answer}</div>', unsafe_allow_html=True)
        
        # 查询输入
        if st.session_state.agent_ready:
            # 检查是否有预设查询
            default_query = st.session_state.get('current_query', '')
            if default_query:
                st.session_state.current_query = ''  # 清除预设查询
                
            query = st.chat_input("请输入您的问题...", key="main_input") or default_query
            
            if query:
                with st.spinner("🔍 正在检索文档..."):
                    try:
                        # 显示用户问题
                        st.markdown(f'<div class="chat-message user-message"><strong>🙋 您：</strong> {query}</div>', unsafe_allow_html=True)
                        
                        # 查询文档
                        start_time = time.time()
                        result = st.session_state.rag_system.query_documents(query)
                        end_time = time.time()
                        
                        # 显示结果
                        st.markdown(f'<div class="chat-message assistant-message"><strong>🤖 助手：</strong> {result}</div>', unsafe_allow_html=True)
                        
                        # 添加到历史记录
                        st.session_state.chat_history.append((query, result))
                        
                        # 显示查询时间
                        st.caption(f"⏱️ 查询耗时: {end_time - start_time:.2f} 秒")
                        
                    except Exception as e:
                        st.error(f"❌ 查询失败: {str(e)}")
        else:
            st.warning("⚠️ 系统未部署，请先部署RAG系统")
            
            if st.button("🚀 部署系统", type="primary"):
                with st.spinner("正在部署系统，请稍候..."):
                    try:
                        # 这里应该调用部署逻辑
                        st.info("请在终端运行: `python enterprise_rag.py --setup` 来部署系统")
                    except Exception as e:
                        st.error(f"部署失败: {str(e)}")
    
    with col2:
        # 系统信息面板
        st.subheader("📊 系统信息")
        
        # 当前时间
        st.write(f"**当前时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 对话统计
        st.write(f"**对话轮次**: {len(st.session_state.chat_history)}")
        
        # 系统状态
        if st.session_state.agent_ready:
            st.success("✅ 系统正常")
        else:
            st.warning("⚠️ 系统未就绪")
            
        st.divider()
        
        # 文档类型
        st.subheader("📚 支持的文档类型")
        doc_types = [
            "📋 公司政策制度",
            "🛠️ IT支持文档", 
            "💰 财务管理制度",
            "👥 人事管理规定",
            "📖 操作手册指南"
        ]
        
        for doc_type in doc_types:
            st.write(doc_type)
            
        st.divider()
        
        # 使用提示
        st.subheader("💡 使用提示")
        tips = [
            "尽量使用具体的关键词",
            "可以询问具体的政策条款",
            "支持中文自然语言查询",
            "可以要求提供操作步骤"
        ]
        
        for tip in tips:
            st.write(f"• {tip}")
    
    # 日志查看（如果需要）
    if st.session_state.get('show_logs', False):
        st.subheader("📋 系统日志")
        try:
            with open("enterprise_rag.log", "r", encoding="utf-8") as f:
                logs = f.read()
                st.text_area("日志内容", logs, height=300)
        except FileNotFoundError:
            st.info("暂无日志文件")
        
        if st.button("关闭日志"):
            st.session_state.show_logs = False
            st.rerun()

if __name__ == "__main__":
    main()
