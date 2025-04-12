# 提交信息规范

## 任务
1. 修改 README.md 文件
2. 使用 Conventional Commits 规范提交
3. 确保信息格式为: `<type>: <description>`

## 验证
```bash
git log -1 --pretty=%B | grep -E "^feat|fix|docs: "
```
