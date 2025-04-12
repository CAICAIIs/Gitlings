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
 
# 4.Gitlings 交互原型

下面是一个完整的终端交互模拟，展示学员如何使用这个系统完成练习，包括普通提示和AI提示的切换。

## 场景1：初始练习引导

```bash
$ gitlings start

==========================================
欢迎来到 Gitlings! (v0.1.0)
==========================================
我们将通过小型练习引导你掌握 Git。

当前进度: 0/20 练习完成
输入 `gitlings hint` 获取帮助
输入 `gitlings verify` 检查你的解答

正在启动第一个练习...
```

## 场景2：基础提交练习

```bash
====================================
练习 1/20: 第一个提交 (难度: ★☆☆)
====================================

■ 任务描述:
1. 初始化一个新的Git仓库
2. 创建 hello.txt 文件，内容为 "Hello Git"
3. 使用规范提交 (feat: add hello.txt)

■ 验证条件:
✓ 仓库初始化完成
✓ hello.txt 存在且内容正确
✓ 提交信息符合 Conventional Commits

[状态] 未完成 ❌

命令选项:
(v) 验证  (h) 提示  (n) 下一个  (s) 解决方案  (q) 退出
> 
```

## 场景3：学员尝试并验证

```bash
> v

[验证结果]
✗ Git 仓库未初始化 (运行 `git init`)
✗ hello.txt 文件不存在
✗ 没有找到符合条件的提交

需要提示吗？ [y/N] y
```

## 场景4：分级提示系统

```bash
选择提示级别:
1. 概念提示 (告诉你需要什么概念)
2. 命令提示 (告诉你相关命令)
3. 详细步骤 (接近答案)
a. 询问AI导师
> 1

[提示] 你需要先创建一个"版本库"，这是Git记录变化的地方。
```

学员尝试后：

```bash
$ git init
初始化空的 Git 仓库于 /home/user/exercises/.git/

> v

[验证结果]
✓ Git 仓库初始化完成
✗ hello.txt 文件不存在
✗ 没有找到符合条件的提交
```

## 场景5：AI提示交互

```bash
> h
选择提示级别: a

[AI导师] 你好！看起来你已经完成了第一步，很棒！
现在需要创建一个文件。在Linux/macOS下可以使用 `echo` 命令，
Windows可以用记事本。你想创建什么内容呢？
(输入你的问题或直接按回车返回) > 怎么写提交信息？

[AI导师] 提交信息就像给更改写个小便签。规范格式是：
`类型: 简短描述`，比如你添加新文件属于新功能(feat)。
试试看写 `feat: add hello.txt` 怎么样？
```

## 场景6：完成练习

```bash
$ echo "Hello Git" > hello.txt
$ git add hello.txt
$ git commit -m "feat: add hello.txt"
[main (root-commit) abc123] feat: add hello.txt
 1 file changed, 1 insertion(+)
 create mode 100644 hello.txt

> v

[验证结果]
✓ Git 仓库初始化完成
✓ hello.txt 存在且内容正确
✓ 找到规范提交: abc123 "feat: add hello.txt"

[反馈] 太棒了！你的第一个规范提交完成得很完美！
(输入 `gitlings next` 进入下一个练习)
```

## 场景7：冲突解决练习 (进阶演示)

```bash
====================================
练习 5/20: 合并冲突 (难度: ★★☆)
====================================

■ 场景:
你和同事同时修改了 README.md 的不同部分
现在需要合并这些更改并解决冲突

■ 任务:
1. 合并 branch 'feature/contact' 到 main
2. 解决 README.md 的冲突
3. 完成合并提交

> h a

[AI导师] 啊，遇到第一个合并冲突了！别担心，这很正常。
Git 用 <<<<<<< 标记冲突位置，你需要:
1. 打开 README.md
2. 保留需要的部分
3. 删除所有标记行
4. 保存后 `git add` 告诉Git冲突已解决

需要我展示冲突文件的样子吗？ [y/N] y

[AI演示]
<<<<<<< HEAD
我们的电话: 123-4567
=======
我们的邮箱: contact@example.com
>>>>>>> feature/contact

应该保留两者，删除标记后变成:
我们的电话: 123-4567
我们的邮箱: contact@example.com
```

## 场景8：错误恢复演示

```bash
$ git merge feature/contact
自动合并 README.md
冲突（内容）：合并冲突于 README.md

> v

[验证结果]
✓ 合并启动 (冲突状态)
✗ README.md 冲突未解决
✗ 没有合并提交

> h a

[AI导师] 看起来你在解决冲突时遇到了困难。要放弃重来吗？
可以运行 `git merge --abort` 重新开始。
或者你想知道具体哪部分有问题？ [放弃/查看冲突] > 查看冲突

[AI导师] 冲突文件包含:
1. 当前分支内容 (HEAD)
2. 要合并的分支内容
你需要决定保留哪些内容。在这个案例中，
联系方式应该都保留，因为它们不冲突。
```

## 技术原型说明

要实现这个交互流程，需要以下核心组件：

1. **练习运行器** (Python示例)
```python
class ExerciseRunner:
    def __init__(self):
        self.current_exercise = load_exercise()
        self.history = []
    
    def verify(self):
        results = []
        for check in self.current_exercise.checks:
            results.append(run_check(check))
        display_results(results)
    
    def show_hint(self, level):
        if level == "ai":
            ai_hint = query_ai(
                context=self.current_exercise,
                user_history=self.history
            )
            display(ai_hint)
        else:
            display(self.current_exercise.hints[level])
```

2. **AI提示服务** (伪代码)
```python
def generate_ai_hint(exercise, user_history):
    prompt = f"""
    你是一个Git导师。学员正在做练习:
    {exercise.description}
    
    他们尝试过:
    {user_history.last_attempts}
    
    最近错误:
    {user_history.last_errors}
    
    请用简单易懂的语言给出提示，不要直接给答案。
    使用比喻和鼓励性语言。
    """
    return query_llm(prompt)
```

3. **终端UI** (使用curses或rich库)
```python
def render_exercise_screen(exercise):
    console.print(Panel.fit(
        f"[bold]{exercise.name}[/]\n\n"
        f"{exercise.description}\n\n"
        f"[验证状态]: {get_status()}",
        title="Gitlings"
    ))
    show_command_prompt()
```

这个原型展示了：
- 渐进式提示系统
- 上下文感知的AI引导
- 真实的Git操作环境
- 友好的学习曲线
- 错误恢复指导

开发时可以先用静态提示实现基础功能，再逐步集成AI组件。
