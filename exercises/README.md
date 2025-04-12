### **1. 配置与初始化 (config)**
**目标**：掌握Git基础配置和仓库初始化

#### 练习列表：
1. **初始化配置**
   - 任务：设置用户名/邮箱，配置默认编辑器为vim
   - 验证：`git config --list` 检查配置项
   - AI提示示例："Git需要知道你是谁，试试`git config --global user.name`命令"

2. **仓库初始化**
   - 任务：创建新仓库，添加.gitignore文件（忽略*.log）
   - 验证：检查.git目录和.gitignore内容
   - 编辑器集成：vim编辑.gitignore文件

3. **别名配置**
   - 任务：创建`git lg`别名显示美化日志
   - 验证：`git lg`能否输出单行日志

---

### **2. 分支与基本操作**
**目标**：掌握分支生命周期管理

#### 练习列表：
1. **基础分支操作**
   ```bash
   # 任务：
   1. 创建feature/login分支
   2. 添加login.py文件并提交
   3. 切回main分支合并
   ```
   - 验证：`git graph`显示合并拓扑图
   - 冲突模拟：自动生成冲突文件（通过脚本）

2. **交互式rebase**
   - 任务：合并多个WIP提交为一个规范提交
   - 编辑器集成：vim编辑交互式rebase列表
   - AI提示："`pick`保留提交，`squash`合并到前一个提交"

3. **紧急修复工作流**
   ```bash
   # 场景：
   1. 在feature分支工作时发现紧急bug
   2. 暂存当前改动(stash)
   3. 创建hotfix分支修复后回到原分支
   ```
   - 关键命令：`git stash`, `git cherry-pick`

---

### **3. 远程协作与冲突解决**
**目标**：模拟团队协作场景

#### 练习列表：
1. **首次协作**
   ```bash
   # 任务：
   1. Fork远程仓库
   2. 克隆本地后添加上游仓库
   3. 推送新分支并创建PR
   ```
   - 验证：`git remote -v`显示正确配置

2. **冲突解决**
   - 自动生成冲突场景：
     ```python
     # 生成器脚本：
     create_conflict_file("README.md", 
       "<<<<<<< HEAD\n你的改动\n=======\n同事的改动\n>>>>>>>")
     ```
   - AI提示："冲突标记之间的内容需要手动选择保留哪些"

3. **代码审查模拟**
   - 任务：根据虚拟评论修改代码（通过注释文件）
   - 编辑器集成：vim打开review.patch文件

---

### **4. 版本控制与标签**
**目标**：掌握发布管理

#### 练习列表：
1. **语义化版本标签**
   - 任务：为当前提交打v1.0.0标签
   - 验证：`git tag -l`显示标签

2. **发布回滚**
   ```bash
   # 场景：
   1. 发现v1.0.0有严重bug
   2. 创建v1.0.1修复版本
   3. 演示`git revert`和`git reset`区别
   ```
   - AI提示："回滚公开提交用`revert`，本地未推送用`reset`"

3. **发布说明生成**
   - 任务：基于Conventional Commits生成CHANGELOG.md
   - 编辑器集成：vim编辑生成的发布说明

---

### **5. 提交规范与Quiz**
**目标**：强化规范意识

#### 练习设计：
1. **提交消息修正**
   - 提供不合规的提交历史：
     ```bash
     git commit -m "fixed bug"
     git commit -m "update"
     ```
   - 任务：使用`git commit --amend`和`git rebase`重写消息

2. **实时提交检查**
   - 预提交钩子：检查消息是否符合Conventional Commits
   - 错误示例：
     ```bash
     # 触发拒绝的提交：
     git commit -m "修改文件"
     ```
   - AI提示："试试`feat: 添加登录功能`这样的格式"

#### Quiz设计（自动评测）：
```python
# 测试用例示例：
def test_commit_message():
    assert is_conventional("feat(login): add OAuth support") 
    assert not is_conventional("fixed bug")  # 应失败

def test_branch_cleanup():
    assert not has_merged_branches()  # 检查是否删除已合并分支
```

---

### **6. 综合实战项目**
**最终考核**：完整工作流模拟

#### 场景设计：
```markdown
# 模拟开源项目贡献：
1. Fork项目 -> 克隆本地
2. 创建feature分支开发新功能
3. 处理同步上游变更产生的冲突
4. 提交符合规范的PR
5. 根据review意见修改代码
6. 打版本标签并生成发布说明
```

#### 验证点：
1. 分支策略正确性
2. 冲突解决完整性
3. 提交消息规范性
4. 版本标签准确性

---

### **特殊设计要素**

1. **Vim深度集成**：
   - 关键操作强制使用vim：
     ```python
     def edit_commit_message():
         os.environ["EDITOR"] = "vim +/^#"
         git.commit("-e")
     ```
   - 内置vim快捷键提示（如`:wq保存退出`）

2. **AI情景化提示**：
   - 根据错误模式动态生成建议：
     ```python
     if "merge conflict" in error:
         ai.generate("冲突解决指南")
     elif "detached HEAD" in error:
         ai.generate("HEAD分离状态恢复方法")
     ```

3. **Docker友好设计**：
   - 所有练习在容器内可重复执行
   - 通过卷映射保留用户进度：
     ```bash
     docker run -v ./progress:/app/progress gitlings
     ```

4. **渐进式难度曲线**：
   ```mermaid
   graph LR
   A[基础配置] --> B[单分支操作]
   B --> C[本地冲突解决]
   C --> D[远程协作]
   D --> E[版本发布]
   E --> F[规范审计]
   ```

### 后续引入

1. 联机功能
2. 基于vim的ide功能
