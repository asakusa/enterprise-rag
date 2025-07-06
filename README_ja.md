# 🏢 企業文書検索RAGシステム

Amazon Bedrockベースのインテリジェント企業文書検索システム。自然言語で企業内部文書を検索できます。

## ✨ 機能特徴

- 🔍 **インテリジェント検索**：Amazon Bedrock Knowledge Baseによるセマンティック検索
- 🤖 **自然な対話**：Amazon Nova Proモデルによる自然言語インタラクション
- 📚 **多文書対応**：Markdown、PDF、Wordなど複数の文書形式をサポート
- 🎨 **フレンドリーなUI**：Streamlitベースのモダンなウェブインターフェース
- 💻 **デュアルモード**：コマンドラインとウェブインターフェースの両方をサポート
- 🔒 **エンタープライズ級**：権限制御とセキュリティ管理をサポート

## 🚀 クイックスタート

### 環境要件

- Python 3.9+
- AWS CLI設定
- 有効なAWSアカウントとBedrock アクセス権限

### 依存関係のインストール

```bash
pip install -r requirements.txt
```

### AWS認証情報の設定

```bash
aws configure
```

### アプリケーションの起動

#### ウェブインターフェースモード（推奨）

```bash
streamlit run web_demo_ja.py --server.port 8501 --server.address 0.0.0.0
```

ブラウザで以下にアクセス：`http://localhost:8501`

#### コマンドラインモード

```bash
# インタラクティブモード
python demo_ja.py

# バッチデモ
python demo_ja.py batch

# 単発クエリ
python demo_ja.py query "あなたの質問"
```

## 📋 サポートされるクエリタイプ

### 🏛️ 会社ポリシークエリ
- "会社の休暇制度は何ですか？"
- "年次有給休暇は何日ありますか？"
- "残業代はどのように計算されますか？"
- "従業員福利厚生にはどのようなものがありますか？"

### 🛠️ ITサポートクエリ
- "ネットワーク接続の問題はどう解決しますか？"
- "VPNの設定方法は？"
- "プリンターの接続方法は？"
- "メール設定の方法は？"

### 💰 財務制度クエリ
- "出張費の精算基準はいくらですか？"
- "設備購入の申請方法は？"
- "財務承認プロセスは何ですか？"
- "予算管理制度は？"

## 📁 プロジェクト構造

```
enterprise-rag/
├── documents/              # 企業文書ディレクトリ
│   ├── company_policy.md   # 会社ポリシーハンドブック
│   ├── it_support.md       # ITサポート文書
│   └── finance_policy.md   # 財務管理制度
├── src/                    # ソースコードディレクトリ
├── config/                 # 設定ファイルディレクトリ
├── demo_ja.py             # コマンドライン日本語デモプログラム
├── web_demo_ja.py         # ウェブインターフェース日本語プログラム
├── requirements.txt        # Python依存関係
├── quick_start.sh         # クイックスタートスクリプト
└── README_ja.md           # 日本語説明文書
```

## 🎨 ウェブインターフェース特徴

- **レスポンシブデザイン**：デスクトップとモバイルデバイスに対応
- **リアルタイム統計**：クエリ回数と平均応答時間を表示
- **サンプル質問**：サイドバーで一般的な質問への素早いアクセス
- **美しい表示**：回答、ソース、応答時間を構造化して表示
- **インタラクティブ**：シンプルで直感的なユーザーインターフェース

## 🔧 設定説明

### コア設定

`demo_ja.py`と`web_demo_ja.py`で以下の設定を変更：

```python
# ナレッジベースID
self.kb_id = "HCDVL6Q0KZ"

# モデルARN
self.model_arn = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0"
```

### AWS権限要件

AWS認証情報に以下の権限があることを確認：
- `bedrock:InvokeModel`
- `bedrock:RetrieveAndGenerate`
- 対応するKnowledge Baseへのアクセス権限

## 📊 システムアーキテクチャ

```
ユーザークエリ → ウェブUI/CLI → Bedrock Agent → Knowledge Base → 文書検索 → 回答生成
```

### コアコンポーネント

1. **Knowledge Base**：企業文書の保存とインデックス
2. **Bedrock Agent**：クエリ処理と回答生成
3. **Nova Pro Model**：自然言語理解能力の提供
4. **Streamlit**：モダンなウェブインターフェースの提供

## 🛠️ 開発ガイド

### 新機能の追加

1. **クエリタイプの拡張**：`query()`メソッドを変更
2. **カスタムインターフェース**：`web_demo_ja.py`のStreamlitコンポーネントを編集
3. **新モデルの追加**：`model_arn`設定を更新

### ローカル開発

```bash
# プロジェクトのクローン
git clone https://github.com/asakusa/enterprise-rag.git
cd enterprise-rag

# 依存関係のインストール
pip install -r requirements.txt

# 開発サーバーの起動
streamlit run web_demo_ja.py --server.runOnSave true
```

## 🔒 セキュリティ考慮事項

- すべてのデータはあなたのAWSアカウントに保存
- IAM権限制御をサポート
- アクセスログと監査の設定が可能
- 本番環境ではVPC内での展開を推奨

## 🛠️ トラブルシューティング

### よくある問題

1. **ModuleNotFoundError**
   ```bash
   pip install -r requirements.txt
   ```

2. **AWS認証情報エラー**
   ```bash
   aws configure
   # または環境変数の設定
   export AWS_ACCESS_KEY_ID=your_key
   export AWS_SECRET_ACCESS_KEY=your_secret
   ```

3. **Knowledge Baseアクセス失敗**
   - `kb_id`が正しいかチェック
   - AWSリージョン設定の確認
   - IAM権限の検証

### ログの確認

```bash
# ウェブモードログ
tail -f streamlit.log

# コマンドラインモードは直接エラー情報を表示
```

## 📈 パフォーマンス最適化

- **応答時間**：通常2-5秒
- **同時接続サポート**：Streamlitは複数ユーザーアクセスをサポート
- **キャッシュメカニズム**：クエリ結果キャッシュの追加が可能
- **負荷分散**：本番環境では複数インスタンス展開を推奨

## 🤝 貢献

IssueとPull Requestの提出を歓迎します！

### 貢献ガイド

1. このプロジェクトをFork
2. 機能ブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. Pull Requestを開く

## 📄 ライセンス

このプロジェクトはMITライセンスでオープンソース化されています - 詳細は[LICENSE](LICENSE)ファイルをご覧ください。

## 🙏 謝辞

- [Amazon Bedrock](https://aws.amazon.com/bedrock/) - 強力なAI機能の提供
- [Streamlit](https://streamlit.io/) - 優秀なPython Webフレームワーク
- [Boto3](https://boto3.amazonaws.com/) - AWS SDK for Python

---

**⭐ このプロジェクトがお役に立ちましたら、スターをお願いします！**

**📧 技術サポート**：問題がございましたら、Issueを提出するか、メンテナーにお問い合わせください。
