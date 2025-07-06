#!/usr/bin/env python3
"""
企业文档检索 RAG 系统 - Web版本
基于 Streamlit 的网页界面
"""

import streamlit as st
import boto3
import time
from datetime import datetime

class EnterpriseRAGDemo:
    def __init__(self):
        self.client = boto3.client('bedrock-agent-runtime')
        self.kb_id = "HCDVL6Q0KZ"
        self.model_arn = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0"
        
    def query(self, question):
        """查询知识库"""
        try:
            start_time = time.time()
            response = self.client.retrieve_and_generate(
                input={'text': question},
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'knowledgeBaseId': self.kb_id,
                        'modelArn': self.model_arn
                    }
                }
            )
            end_time = time.time()
            
            answer = response['output']['text']
            citations = []
            
            # 提取引用来源
            for citation in response.get('citations', []):
                for ref in citation.get('retrievedReferences', []):
                    source = ref.get('location', {}).get('s3Location', {}).get('uri', '')
                    if source:
                        filename = source.split('/')[-1]
                        citations.append(filename)
            
            return {
                'answer': answer,
                'citations': list(set(citations)),
                'response_time': end_time - start_time
            }
            
        except Exception as e:
            return {'error': str(e)}

def main():
    # 页面配置
    st.set_page_config(
        page_title="企业文档检索 RAG 系统",
        page_icon="🏢",
        layout="wide"
    )
    
    # 初始化RAG系统
    if 'rag_demo' not in st.session_state:
        st.session_state.rag_demo = EnterpriseRAGDemo()
    
    # 页面标题
    st.title("🏢 企业文档检索 RAG 系统")
    st.markdown("---")
    
    # 侧边栏信息
    with st.sidebar:
        st.header("📋 系统信息")
        st.info(f"**知识库 ID:** {st.session_state.rag_demo.kb_id}")
        st.info("**使用模型:** Amazon Nova Pro")
        
        st.header("💡 示例问题")
        example_questions = [
            "公司的请假制度是什么？",
            "如何设置VPN连接？",
            "差旅费报销标准是多少？",
            "加班工资如何计算？",
            "网络连接问题怎么解决？",
            "财务审批流程是什么？"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"example_{question}"):
                st.session_state.current_question = question
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🙋 提问区域")
        
        # 获取当前问题
        current_question = st.session_state.get('current_question', '')
        
        # 问题输入框
        question = st.text_area(
            "请输入您的问题：",
            value=current_question,
            height=100,
            placeholder="例如：公司的请假制度是什么？"
        )
        
        # 查询按钮
        if st.button("🔍 查询", type="primary"):
            if question.strip():
                with st.spinner("正在查询，请稍候..."):
                    result = st.session_state.rag_demo.query(question)
                    st.session_state.last_result = result
                    st.session_state.last_question = question
            else:
                st.warning("请输入问题后再查询")
    
    with col2:
        st.header("📊 查询统计")
        
        # 初始化统计数据
        if 'query_count' not in st.session_state:
            st.session_state.query_count = 0
        if 'total_time' not in st.session_state:
            st.session_state.total_time = 0
        
        st.metric("查询次数", st.session_state.query_count)
        if st.session_state.query_count > 0:
            avg_time = st.session_state.total_time / st.session_state.query_count
            st.metric("平均响应时间", f"{avg_time:.2f}秒")
    
    # 显示查询结果
    if 'last_result' in st.session_state and 'last_question' in st.session_state:
        st.markdown("---")
        st.header("🤖 查询结果")
        
        result = st.session_state.last_result
        question = st.session_state.last_question
        
        # 显示问题
        st.subheader(f"🔍 问题: {question}")
        
        if 'error' in result:
            st.error(f"❌ 查询失败: {result['error']}")
        else:
            # 更新统计数据
            st.session_state.query_count += 1
            st.session_state.total_time += result['response_time']
            
            # 显示答案
            st.success("✅ 查询成功")
            
            # 答案区域
            with st.container():
                st.markdown("**📝 回答:**")
                st.markdown(result['answer'])
            
            # 引用来源
            if result['citations']:
                st.markdown("**📚 信息来源:**")
                for citation in result['citations']:
                    st.markdown(f"- {citation}")
            
            # 响应时间
            st.markdown(f"**⏱️ 响应时间:** {result['response_time']:.2f} 秒")
    
    # 页脚
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🏢 企业文档检索 RAG 系统 | 基于 Amazon Bedrock Knowledge Base</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
