#!/bin/bash

echo "🏢 企業文書検索RAGシステム（日本語版）"
echo "=================================="

# 使用方法の表示
show_usage() {
    echo "使用方法:"
    echo "  ./start_ja.sh web     - ウェブインターフェースを起動"
    echo "  ./start_ja.sh cli     - コマンドラインデモを起動"
    echo "  ./start_ja.sh batch   - バッチデモを実行"
    echo "  ./start_ja.sh query   - 単発クエリを実行"
    echo ""
    echo "例:"
    echo "  ./start_ja.sh web"
    echo "  ./start_ja.sh query \"会社の休暇制度は何ですか？\""
}

# 依存関係のチェック
check_dependencies() {
    echo "📦 依存関係をチェック中..."
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3がインストールされていません"
        exit 1
    fi
    
    if ! python3 -c "import boto3" &> /dev/null; then
        echo "❌ boto3がインストールされていません"
        echo "💡 pip install -r requirements.txt を実行してください"
        exit 1
    fi
    
    if ! python3 -c "import streamlit" &> /dev/null; then
        echo "❌ streamlitがインストールされていません"
        echo "💡 pip install -r requirements.txt を実行してください"
        exit 1
    fi
    
    echo "✅ 依存関係OK"
}

# ウェブインターフェースの起動
start_web() {
    echo "🌐 ウェブインターフェースを起動中..."
    echo "📍 ブラウザで http://localhost:8501 にアクセスしてください"
    echo "⏹️  停止するには Ctrl+C を押してください"
    echo ""
    
    streamlit run web_demo_ja.py --server.port 8501 --server.address 0.0.0.0
}

# コマンドラインデモの起動
start_cli() {
    echo "💻 コマンドラインデモを起動中..."
    echo ""
    
    python3 demo_ja.py
}

# バッチデモの実行
start_batch() {
    echo "📋 バッチデモを実行中..."
    echo ""
    
    python3 demo_ja.py batch
}

# 単発クエリの実行
run_query() {
    if [ -z "$2" ]; then
        echo "❌ 質問を指定してください"
        echo "例: ./start_ja.sh query \"会社の休暇制度は何ですか？\""
        exit 1
    fi
    
    echo "🔍 クエリを実行中..."
    echo ""
    
    python3 demo_ja.py query "$2"
}

# メイン処理
main() {
    check_dependencies
    
    case "$1" in
        "web")
            start_web
            ;;
        "cli")
            start_cli
            ;;
        "batch")
            start_batch
            ;;
        "query")
            run_query "$@"
            ;;
        *)
            show_usage
            ;;
    esac
}

# スクリプト実行
main "$@"
