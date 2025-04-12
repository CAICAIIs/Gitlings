## 开发须知

1. 使用conventional commits+emojis+正文(表情可复用,应对你一次性的混乱提交

2. commit 正文不要少于100单词或200字,说明为什么改,改了什么,影响范围(即WWI原则)

3. 早期使用github flow和GitFlow的项目维护方式,

   - ^1. main 分支：稳定版，仅通过 PR 合并
   - ^2. 新功能或修复在 feature/xxx 或 fix/xxx 分支开发
   - ^3. 提交 PR → Code Review → CI 测试 → 合并

4. 创建分支时遵守以下命名规范:

   | 分支          | 用途           |
   | ------------- | -------------- |
   | `main`        | 生产环境稳定版 |
   | `develop`     | 开发主线       |
   | `feature/xxx` | 新功能开发     |
   | `release/xxx` | 预发布测试     |
   | `hotfix/xxx`  | 紧急修复       |

****

5. 对于提交规范
   - **`rebase` 代替 `merge`**（保持线性历史）
   - **交互式变基（`git rebase -i`）** 整理提交记录,或者偶尔的cherry-pick也行
   - **`--signoff` 签署提交**

4. issue
5. pr规范和ci检查规则