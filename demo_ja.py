#!/usr/bin/env python3
"""
企業文書検索RAGシステムデモ（日本語版）
"""

import boto3
import time
import sys
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
    
    def interactive_demo(self):
        """インタラクティブデモ"""
        print("🏢 企業文書検索RAGシステムデモ")
        print("=" * 50)
        print("Amazon Bedrock Knowledge Baseベース")
        print(f"ナレッジベースID: {self.kb_id}")
        print(f"使用モデル: Amazon Nova Pro")
        print("=" * 50)
        
        while True:
            print("\n💡 以下のタイプの質問ができます：")
            print("📋 会社ポリシー：休暇制度、給与福利厚生、行動規範")
            print("🛠️ ITサポート：ネットワーク問題、VPN設定、ソフトウェアインストール")
            print("💰 財務制度：精算基準、承認プロセス、予算管理")
            print("\n'quit'を入力するとデモを終了します")
            
            question = input("\n🙋 質問を入力してください: ").strip()
            
            if question.lower() in ['quit', 'exit', '終了', 'やめる']:
                print("👋 企業文書検索システムをご利用いただき、ありがとうございました！")
                break
                
            if not question:
                continue
                
            print(f"\n🔍 検索中: {question}")
            print("⏳ しばらくお待ちください...")
            
            result = self.query(question)
            
            if 'error' in result:
                print(f"❌ クエリ失敗: {result['error']}")
                continue
                
            print("\n" + "=" * 60)
            print("🤖 回答:")
            print(result['answer'])
            
            if result['citations']:
                print(f"\n📚 情報ソース: {', '.join(result['citations'])}")
                
            print(f"\n⏱️ 応答時間: {result['response_time']:.2f} 秒")
            print("=" * 60)
    
    def batch_demo(self):
        """バッチデモ"""
        print("🏢 企業文書検索RAGシステム - バッチデモ")
        print("=" * 50)
        
        demo_questions = [
            "会社の休暇制度は何ですか？",
            "VPN接続の設定方法は？", 
            "出張費精算基準はいくらですか？",
            "残業代はどのように計算されますか？",
            "ネットワーク接続問題はどう解決しますか？",
            "財務承認プロセスは何ですか？"
        ]
        
        for i, question in enumerate(demo_questions, 1):
            print(f"\n📋 デモ {i}/{len(demo_questions)}: {question}")
            print("-" * 50)
            
            result = self.query(question)
            
            if 'error' in result:
                print(f"❌ クエリ失敗: {result['error']}")
                continue
                
            print("🤖 回答:")
            print(result['answer'])
            
            if result['citations']:
                print(f"\n📚 ソース: {', '.join(result['citations'])}")
                
            print(f"⏱️ 所要時間: {result['response_time']:.2f}秒")
            
            if i < len(demo_questions):
                input("\nEnterキーを押して次のデモに進む...")
        
        print("\n✅ バッチデモ完了！")

def main():
    demo = EnterpriseRAGDemo()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'batch':
            demo.batch_demo()
        elif sys.argv[1] == 'query' and len(sys.argv) > 2:
            question = ' '.join(sys.argv[2:])
            result = demo.query(question)
            
            if 'error' in result:
                print(f"❌ クエリ失敗: {result['error']}")
            else:
                print(f"🔍 質問: {question}")
                print("=" * 50)
                print(result['answer'])
                if result['citations']:
                    print(f"\n📚 ソース: {', '.join(result['citations'])}")
                print(f"\n⏱️ 所要時間: {result['response_time']:.2f}秒")
        else:
            print("使用方法:")
            print("  python demo_ja.py                    - インタラクティブデモ")
            print("  python demo_ja.py batch              - バッチデモ")
            print("  python demo_ja.py query \"あなたの質問\"  - 単発クエリ")
    else:
        demo.interactive_demo()

if __name__ == "__main__":
    main()
