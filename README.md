# Gitlings 技术架构方案


## 1. 项目架构设计

```
gitlings-repo/
├── .gitmodules                # 子模块管理
├── gitlings/                  # 主包
│   ├── cli/                   # 命令行接口
│   │   └── __main__.py        # 主入口
│   ├── core/                  # 核心逻辑
│   │   ├── exercise.py        # 练习管理
│   │   ├── verifier.py        # 验证逻辑
│   │   └── git_utils.py       # Git操作封装
│   ├── ai/                    # AI提示服务
│   │   ├── hint_generator.py  # 提示生成
│   │   └── llm_integration.py # 大模型接口
│   └── utils/                 # 工具类
│       ├── editor.py          # 编辑器集成
│       └── ui.py              # 终端UI
├── exercises/                 # 练习定义
│   ├── basic/
│   │   ├── 01_init/
│   │   │   ├── meta.toml
│   │   │   └── exercise.md
│   │   └── ...
│   └── advanced/
├── tests/                     # 测试
├── pyproject.toml             # 项目配置
├── Dockerfile                 # Docker构建
└── README.md                  # 项目文档
```

## 2. 核心技术选型

| 组件          | 技术选择                  | 理由                                                                 |
|---------------|--------------------------|----------------------------------------------------------------------|
| 语言          | Python 3.10+             | 适合CLI开发，丰富的Git库支持                                         |
| Git操作       | GitPython + dulwich      | GitPython提供高级API，dulwich提供纯Python实现作为后备                 |
| 终端UI        | Rich + Textual           | 丰富的终端渲染能力，支持交互式元素                                    |
| 编辑器集成    | click.edit() + envvar    | 支持$EDITOR环境变量，默认vim优先                                     |
| 配置管理      | TOML                     | 比JSON更易读，比YAML更简单                                           |
| AI集成        | llama-index + 开放API    | 支持多模型后端，本地可运行LLM                                        |
| 打包          | Poetry                   | 现代Python打包工具，依赖管理优秀                                     |
| 测试          | pytest + tox             | 标准测试工具链                                                       |


# 3. exercises 内容

- config
- 分支和基本操作
- 远程冲突解决和团队协作
- 版本控制和标签管理
- 提交规范和quiz
