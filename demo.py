#!/usr/bin/env python3
"""
企业文档检索 RAG 系统演示
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
    
    def interactive_demo(self):
        """交互式演示"""
        print("🏢 企业文档检索 RAG 系统演示")
        print("=" * 50)
        print("基于 Amazon Bedrock Knowledge Base")
        print(f"知识库 ID: {self.kb_id}")
        print(f"使用模型: Amazon Nova Pro")
        print("=" * 50)
        
        while True:
            print("\n💡 您可以询问以下类型的问题：")
            print("📋 公司政策：请假制度、薪酬福利、行为规范")
            print("🛠️ IT支持：网络问题、VPN设置、软件安装")
            print("💰 财务制度：报销标准、审批流程、预算管理")
            print("\n输入 'quit' 退出演示")
            
            question = input("\n🙋 请输入您的问题: ").strip()
            
            if question.lower() in ['quit', 'exit', '退出']:
                print("👋 感谢使用企业文档检索系统！")
                break
                
            if not question:
                continue
                
            print(f"\n🔍 正在查询: {question}")
            print("⏳ 请稍候...")
            
            result = self.query(question)
            
            if 'error' in result:
                print(f"❌ 查询失败: {result['error']}")
                continue
                
            print("\n" + "=" * 60)
            print("🤖 回答:")
            print(result['answer'])
            
            if result['citations']:
                print(f"\n📚 信息来源: {', '.join(result['citations'])}")
                
            print(f"\n⏱️ 响应时间: {result['response_time']:.2f} 秒")
            print("=" * 60)
    
    def batch_demo(self):
        """批量演示"""
        print("🏢 企业文档检索 RAG 系统 - 批量演示")
        print("=" * 50)
        
        demo_questions = [
            "公司的请假制度是什么？",
            "如何设置VPN连接？", 
            "差旅费报销标准是多少？",
            "加班工资如何计算？",
            "网络连接问题怎么解决？",
            "财务审批流程是什么？"
        ]
        
        for i, question in enumerate(demo_questions, 1):
            print(f"\n📋 演示 {i}/{len(demo_questions)}: {question}")
            print("-" * 50)
            
            result = self.query(question)
            
            if 'error' in result:
                print(f"❌ 查询失败: {result['error']}")
                continue
                
            print("🤖 回答:")
            print(result['answer'])
            
            if result['citations']:
                print(f"\n📚 来源: {', '.join(result['citations'])}")
                
            print(f"⏱️ 耗时: {result['response_time']:.2f}秒")
            
            if i < len(demo_questions):
                input("\n按回车键继续下一个演示...")
        
        print("\n✅ 批量演示完成！")

def main():
    demo = EnterpriseRAGDemo()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'batch':
            demo.batch_demo()
        elif sys.argv[1] == 'query' and len(sys.argv) > 2:
            question = ' '.join(sys.argv[2:])
            result = demo.query(question)
            
            if 'error' in result:
                print(f"❌ 查询失败: {result['error']}")
            else:
                print(f"🔍 问题: {question}")
                print("=" * 50)
                print(result['answer'])
                if result['citations']:
                    print(f"\n📚 来源: {', '.join(result['citations'])}")
                print(f"\n⏱️ 耗时: {result['response_time']:.2f}秒")
        else:
            print("用法:")
            print("  python demo.py                    - 交互式演示")
            print("  python demo.py batch              - 批量演示")
            print("  python demo.py query \"您的问题\"    - 单次查询")
    else:
        demo.interactive_demo()

if __name__ == "__main__":
    main()
