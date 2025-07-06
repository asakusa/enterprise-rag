#!/bin/bash

echo "🚀 准备推送到GitHub..."

# 检查是否已经添加了远程仓库
if git remote get-url origin 2>/dev/null; then
    echo "✅ 远程仓库已存在"
else
    echo "📡 添加远程仓库..."
    git remote add origin https://github.com/asakusa/enterprise-rag.git
fi

echo "📤 推送代码到GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "🎉 成功推送到GitHub!"
    echo "🌐 访问: https://github.com/asakusa/enterprise-rag"
else
    echo "❌ 推送失败，请检查："
    echo "1. GitHub仓库是否已创建"
    echo "2. 网络连接是否正常"
    echo "3. Git凭证是否正确"
fi
