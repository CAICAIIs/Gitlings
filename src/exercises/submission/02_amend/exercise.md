# 修改提交

## 任务
1. 创建一个不完整的提交（忘记添加某个文件）
2. 使用 --amend 修正这个提交
3. 检查修正后的提交历史

## 验证
```bash
git log -1 --stat | grep "both files"
```
