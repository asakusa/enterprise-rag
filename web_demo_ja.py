#!/usr/bin/env python3
"""
企業文書検索RAGシステム - ウェブ版（日本語）
Streamlitベースのウェブインターフェース
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
        """ナレッジベースにクエリ"""
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
            
            # 引用ソースの抽出
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
    # ページ設定
    st.set_page_config(
        page_title="企業文書検索RAGシステム",
        page_icon="🏢",
        layout="wide"
    )
    
    # RAGシステムの初期化
    if 'rag_demo' not in st.session_state:
        st.session_state.rag_demo = EnterpriseRAGDemo()
    
    # ページタイトル
    st.title("🏢 企業文書検索RAGシステム")
    st.markdown("---")
    
    # サイドバー情報
    with st.sidebar:
        st.header("📋 システム情報")
        st.info(f"**ナレッジベースID:** {st.session_state.rag_demo.kb_id}")
        st.info("**使用モデル:** Amazon Nova Pro")
        
        st.header("💡 サンプル質問")
        example_questions = [
            "会社の休暇制度は何ですか？",
            "VPN接続の設定方法は？",
            "出張費精算基準はいくらですか？",
            "残業代はどのように計算されますか？",
            "ネットワーク接続問題はどう解決しますか？",
            "財務承認プロセスは何ですか？"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"example_{question}"):
                st.session_state.current_question = question
    
    # メインインターフェース
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🙋 質問エリア")
        
        # 現在の質問を取得
        current_question = st.session_state.get('current_question', '')
        
        # 質問入力ボックス
        question = st.text_area(
            "質問を入力してください：",
            value=current_question,
            height=100,
            placeholder="例：会社の休暇制度は何ですか？"
        )
        
        # 検索ボタン
        if st.button("🔍 検索", type="primary"):
            if question.strip():
                with st.spinner("検索中です。しばらくお待ちください..."):
                    result = st.session_state.rag_demo.query(question)
                    st.session_state.last_result = result
                    st.session_state.last_question = question
            else:
                st.warning("質問を入力してから検索してください")
    
    with col2:
        st.header("📊 クエリ統計")
        
        # 統計データの初期化
        if 'query_count' not in st.session_state:
            st.session_state.query_count = 0
        if 'total_time' not in st.session_state:
            st.session_state.total_time = 0
        
        st.metric("クエリ回数", st.session_state.query_count)
        if st.session_state.query_count > 0:
            avg_time = st.session_state.total_time / st.session_state.query_count
            st.metric("平均応答時間", f"{avg_time:.2f}秒")
    
    # クエリ結果の表示
    if 'last_result' in st.session_state and 'last_question' in st.session_state:
        st.markdown("---")
        st.header("🤖 検索結果")
        
        result = st.session_state.last_result
        question = st.session_state.last_question
        
        # 質問の表示
        st.subheader(f"🔍 質問: {question}")
        
        if 'error' in result:
            st.error(f"❌ クエリ失敗: {result['error']}")
        else:
            # 統計データの更新
            st.session_state.query_count += 1
            st.session_state.total_time += result['response_time']
            
            # 回答の表示
            st.success("✅ 検索成功")
            
            # 回答エリア
            with st.container():
                st.markdown("**📝 回答:**")
                st.markdown(result['answer'])
            
            # 引用ソース
            if result['citations']:
                st.markdown("**📚 情報ソース:**")
                for citation in result['citations']:
                    st.markdown(f"- {citation}")
            
            # 応答時間
            st.markdown(f"**⏱️ 応答時間:** {result['response_time']:.2f} 秒")
    
    # フッター
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🏢 企業文書検索RAGシステム | Amazon Bedrock Knowledge Baseベース</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
