# 变基操作

## 任务
1. 在main分支上做基础提交
2. 在feature分支开发
3. 使用rebase保持线性历史

## 验证
```bash
git log --oneline --graph | grep -A 1 "feature"
```
