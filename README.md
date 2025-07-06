# 🏢 企业文档检索 RAG 系统

基于 Amazon Bedrock 的智能企业文档检索系统，支持自然语言查询企业内部文档。

## ✨ 功能特点

- 🔍 **智能检索**：基于 Amazon Bedrock Knowledge Base 的语义检索
- 🤖 **自然对话**：使用 Amazon Nova Pro 模型进行自然语言交互
- 📚 **多文档支持**：支持 Markdown、PDF、Word 等多种文档格式
- 🎨 **友好界面**：基于 Streamlit 的现代化 Web 界面
- 💻 **双模式运行**：支持命令行和Web界面两种使用方式
- 🔒 **企业级**：支持权限控制和安全管理

## 🚀 快速开始

### 环境要求

- Python 3.9+
- AWS CLI 配置
- 有效的 AWS 账户和 Bedrock 访问权限

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置 AWS 凭证

```bash
aws configure
```

### 启动应用

#### Web 界面模式（推荐）

```bash
streamlit run web_demo.py --server.port 8501 --server.address 0.0.0.0
```

然后在浏览器中访问：`http://localhost:8501`

#### 命令行模式

```bash
# 交互式模式
python demo.py

# 批量演示
python demo.py batch

# 单次查询
python demo.py query "您的问题"
```

## 📋 支持的查询类型

### 🏛️ 公司政策查询
- "公司的请假制度是什么？"
- "年假有多少天？"
- "加班工资如何计算？"
- "员工福利有哪些？"

### 🛠️ IT支持查询
- "网络连接问题怎么解决？"
- "如何设置VPN？"
- "打印机怎么连接？"
- "邮箱配置方法？"

### 💰 财务制度查询
- "差旅费报销标准是多少？"
- "如何申请设备采购？"
- "财务审批流程是什么？"
- "预算管理制度？"

## 📁 项目结构

```
enterprise-rag/
├── documents/              # 企业文档目录
│   ├── company_policy.md   # 公司政策手册
│   ├── it_support.md       # IT支持文档
│   └── finance_policy.md   # 财务管理制度
├── src/                    # 源代码目录
├── config/                 # 配置文件目录
├── demo.py                 # 命令行演示程序
├── web_demo.py            # Web界面程序
├── requirements.txt        # Python依赖
├── quick_start.sh         # 快速启动脚本
└── README.md              # 说明文档
```

## 🎨 Web 界面特性

- **响应式设计**：适配桌面和移动设备
- **实时统计**：显示查询次数和平均响应时间
- **示例问题**：侧边栏提供常用问题快速访问
- **美观展示**：结构化显示答案、来源和响应时间
- **交互友好**：简洁直观的用户界面

## 🔧 配置说明

### 核心配置

在 `demo.py` 和 `web_demo.py` 中修改以下配置：

```python
# 知识库 ID
self.kb_id = "HCDVL6Q0KZ"

# 模型 ARN
self.model_arn = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0"
```

### AWS 权限要求

确保您的 AWS 凭证具有以下权限：
- `bedrock:InvokeModel`
- `bedrock:RetrieveAndGenerate`
- 对应 Knowledge Base 的访问权限

## 📊 系统架构

```
用户查询 → Web界面/CLI → Bedrock Agent → Knowledge Base → 文档检索 → 答案生成
```

### 核心组件

1. **Knowledge Base**：存储和索引企业文档
2. **Bedrock Agent**：处理查询和生成回答
3. **Nova Pro Model**：提供自然语言理解能力
4. **Streamlit**：提供现代化Web界面

## 🛠️ 开发指南

### 添加新功能

1. **扩展查询类型**：修改 `query()` 方法
2. **自定义界面**：编辑 `web_demo.py` 中的 Streamlit 组件
3. **添加新模型**：更新 `model_arn` 配置

### 本地开发

```bash
# 克隆项目
git clone https://github.com/asakusa/enterprise-rag.git
cd enterprise-rag

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
streamlit run web_demo.py --server.runOnSave true
```

## 🔒 安全考虑

- 所有数据存储在您的AWS账户中
- 支持IAM权限控制
- 可配置访问日志和审计
- 建议在VPC内部署生产环境

## 🛠️ 故障排除

### 常见问题

1. **ModuleNotFoundError**
   ```bash
   pip install -r requirements.txt
   ```

2. **AWS 凭证错误**
   ```bash
   aws configure
   # 或设置环境变量
   export AWS_ACCESS_KEY_ID=your_key
   export AWS_SECRET_ACCESS_KEY=your_secret
   ```

3. **Knowledge Base 访问失败**
   - 检查 `kb_id` 是否正确
   - 确认 AWS 区域设置
   - 验证 IAM 权限

### 日志查看

```bash
# Web模式日志
tail -f streamlit.log

# 命令行模式会直接显示错误信息
```

## 📈 性能优化

- **响应时间**：通常 2-5 秒
- **并发支持**：Streamlit 支持多用户访问
- **缓存机制**：可添加查询结果缓存
- **负载均衡**：生产环境建议使用多实例部署

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Amazon Bedrock](https://aws.amazon.com/bedrock/) - 提供强大的AI能力
- [Streamlit](https://streamlit.io/) - 优秀的Python Web框架
- [Boto3](https://boto3.amazonaws.com/) - AWS SDK for Python

---

**⭐ 如果这个项目对您有帮助，请给个星标支持！**

**📧 技术支持**：如有问题，请提交 Issue 或联系维护者。
