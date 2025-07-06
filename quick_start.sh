#!/bin/bash

# 企业RAG系统快速启动脚本

echo "🏢 企业文档检索RAG系统"
echo "========================"

# 设置工作目录
cd /home/ec2-user/enterprise-rag

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source /home/ec2-user/amazon-bedrock-agent-workshop-for-gcr/.venv/bin/activate

# 检查参数
if [ "$1" = "setup" ]; then
    echo "🚀 开始部署RAG系统..."
    python src/enterprise_rag.py --setup --documents documents/
    echo "✅ 系统部署完成！"
    
elif [ "$1" = "ui" ]; then
    echo "🎨 启动Web界面..."
    echo "界面地址: http://localhost:8501"
    streamlit run src/enterprise_ui.py --server.port 8501 --server.address 0.0.0.0
    
elif [ "$1" = "query" ]; then
    if [ -z "$2" ]; then
        echo "❌ 请提供查询问题"
        echo "用法: ./quick_start.sh query \"您的问题\""
        exit 1
    fi
    echo "🔍 查询: $2"
    python src/enterprise_rag.py --query "$2"
    
elif [ "$1" = "cleanup" ]; then
    echo "🗑️ 清理系统资源..."
    python src/enterprise_rag.py --cleanup
    echo "✅ 清理完成！"
    
else
    echo "用法:"
    echo "  ./quick_start.sh setup     - 部署RAG系统"
    echo "  ./quick_start.sh ui        - 启动Web界面"
    echo "  ./quick_start.sh query \"问题\" - 命令行查询"
    echo "  ./quick_start.sh cleanup   - 清理资源"
    echo ""
    echo "示例:"
    echo "  ./quick_start.sh setup"
    echo "  ./quick_start.sh ui"
    echo "  ./quick_start.sh query \"公司的请假制度是什么？\""
fi
