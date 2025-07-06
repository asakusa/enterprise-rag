#!/usr/bin/env python3
"""
企业文档检索 RAG 系统 - 修复版
"""

import sys
import os
import time
import boto3
import logging
from pathlib import Path

# 添加原项目路径
sys.path.append('/home/ec2-user/amazon-bedrock-agent-workshop-for-gcr')
from src.utils.knowledge_base_helper import KnowledgeBasesForAmazonBedrock
from src.utils.bedrock_agent import Agent

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("enterprise_rag.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnterpriseRAGFixed:
    def __init__(self):
        self.kb_helper = KnowledgeBasesForAmazonBedrock()
        self.s3_client = boto3.client('s3')
        self.bedrock_client = boto3.client('bedrock-agent-runtime')
        
        # 使用现有的S3存储桶
        self.bucket_name = "general-mortgage-kb-1033-7989-1751782957"
        self.kb_name = "enterprise-document-kb"
        self.agent_name = "enterprise_document_assistant"
        
        self.kb_id = None
        self.ds_id = None
        self.agent_id = None
        self.agent_alias_id = None
        
    def upload_documents(self, documents_path):
        """上传企业文档到现有S3存储桶"""
        logger.info(f"开始上传文档从 {documents_path} 到 {self.bucket_name}")
        
        for root, dirs, files in os.walk(documents_path):
            for file in files:
                if file.endswith(('.md', '.txt', '.pdf', '.docx')):
                    file_path = os.path.join(root, file)
                    s3_key = f"enterprise_documents/{file}"
                    
                    logger.info(f"上传文件: {file_path} -> s3://{self.bucket_name}/{s3_key}")
                    self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
                    
    def create_knowledge_base(self):
        """创建企业知识库"""
        logger.info("创建企业知识库...")
        
        # 使用现有的方法签名
        self.kb_id, self.ds_id = self.kb_helper.create_or_retrieve_knowledge_base(
            self.kb_name,
            kb_description="企业内部文档知识库，包含公司政策、IT支持、财务制度等文档",
            data_bucket_name=self.bucket_name
        )
        
        logger.info(f"知识库创建成功: KB ID={self.kb_id}, DS ID={self.ds_id}")
        return self.bucket_name
        
    def sync_knowledge_base(self):
        """同步知识库数据"""
        logger.info("开始同步知识库数据...")
        self.kb_helper.synchronize_data(self.kb_id, self.ds_id)
        logger.info("知识库同步完成")
        
    def create_rag_agent(self):
        """创建RAG Agent"""
        logger.info("创建企业文档检索Agent...")
        
        agent = Agent.create(
            name=self.agent_name,
            role="企业文档检索助手",
            goal="帮助员工快速检索和查询企业内部文档信息",
            instructions="""
            你是一个专业的企业文档检索助手，能够帮助员工查询企业内部文档。
            
            你的主要职责：
            1. 检索企业政策、制度和规定
            2. 提供IT支持和技术指导
            3. 解答财务管理相关问题
            4. 协助员工了解公司流程
            
            回答要求：
            - 基于知识库中的准确信息回答
            - 提供清晰、结构化的答案
            - 如果信息不完整，明确说明
            - 使用友好、专业的语调
            
            如果知识库中没有相关信息，请诚实告知用户，不要编造信息。
            """,
            kb_id=self.kb_id,
            kb_descr="企业内部文档知识库，包含公司政策、IT支持、财务制度等文档",
            llm="us.amazon.nova-pro-v1:0",
            verbose=True
        )
        
        self.agent_id = agent.agent_id
        self.agent_alias_id = agent.agent_alias_id
        
        logger.info(f"Agent创建成功: ID={self.agent_id}, Alias ID={self.agent_alias_id}")
        return agent
        
    def query_documents(self, question):
        """查询文档"""
        if not self.agent_id or not self.agent_alias_id:
            raise ValueError("Agent未初始化，请先创建Agent")
            
        logger.info(f"处理查询: {question}")
        
        try:
            response = self.bedrock_client.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                sessionId=f"session-{int(time.time())}",
                inputText=question
            )
            
            # 解析响应
            result = ""
            for event in response['completion']:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        result += chunk['bytes'].decode('utf-8')
                        
            logger.info(f"查询完成，响应长度: {len(result)}")
            return result
            
        except Exception as e:
            logger.error(f"查询失败: {str(e)}")
            raise
            
    def setup_complete_system(self, documents_path):
        """完整设置RAG系统"""
        logger.info("开始设置企业RAG系统...")
        
        # 1. 上传文档到现有存储桶
        self.upload_documents(documents_path)
        
        # 2. 创建知识库
        self.create_knowledge_base()
        
        # 3. 等待文档上传完成
        logger.info("等待文档处理完成...")
        time.sleep(10)
        
        # 4. 同步知识库
        self.sync_knowledge_base()
        
        # 5. 等待同步完成
        logger.info("等待知识库同步完成...")
        time.sleep(30)
        
        # 6. 创建Agent
        agent = self.create_rag_agent()
        
        logger.info("企业RAG系统设置完成！")
        return agent
        
    def cleanup(self):
        """清理资源"""
        logger.info("开始清理资源...")
        
        if self.agent_id:
            try:
                Agent.delete_by_name(self.agent_name, verbose=True)
                logger.info("Agent删除成功")
            except Exception as e:
                logger.error(f"删除Agent失败: {e}")
                
        if self.kb_id:
            try:
                self.kb_helper.delete_kb(self.kb_name, delete_s3_bucket=False)
                logger.info("知识库删除成功")
            except Exception as e:
                logger.error(f"删除知识库失败: {e}")
                
        logger.info("资源清理完成")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='企业文档检索RAG系统')
    parser.add_argument('--setup', action='store_true', help='设置RAG系统')
    parser.add_argument('--query', type=str, help='查询问题')
    parser.add_argument('--cleanup', action='store_true', help='清理资源')
    parser.add_argument('--documents', type=str, default='../documents', help='文档目录路径')
    
    args = parser.parse_args()
    
    rag = EnterpriseRAGFixed()
    
    try:
        if args.setup:
            # 设置系统
            documents_path = os.path.abspath(args.documents)
            if not os.path.exists(documents_path):
                logger.error(f"文档目录不存在: {documents_path}")
                return
                
            agent = rag.setup_complete_system(documents_path)
            print(f"\n✅ 企业RAG系统设置完成！")
            print(f"Agent ID: {agent.agent_id}")
            print(f"Agent Alias ID: {agent.agent_alias_id}")
            print(f"知识库 ID: {rag.kb_id}")
            print(f"S3 存储桶: {rag.bucket_name}")
            
        elif args.query:
            # 查询文档
            if not rag.agent_id:
                # 尝试获取现有Agent信息
                try:
                    from src.utils.bedrock_agent import agents_helper
                    rag.agent_id = agents_helper.get_agent_id_by_name(rag.agent_name)
                    rag.agent_alias_id = agents_helper.get_agent_latest_alias_id(rag.agent_id)
                except:
                    logger.error("未找到现有Agent，请先运行 --setup")
                    return
                    
            result = rag.query_documents(args.query)
            print(f"\n📋 查询结果：")
            print("=" * 50)
            print(result)
            print("=" * 50)
            
        elif args.cleanup:
            # 清理资源
            rag.cleanup()
            print("✅ 资源清理完成")
            
        else:
            print("请指定操作: --setup, --query 或 --cleanup")
            
    except Exception as e:
        logger.error(f"操作失败: {str(e)}")
        print(f"❌ 操作失败: {str(e)}")

if __name__ == "__main__":
    main()
