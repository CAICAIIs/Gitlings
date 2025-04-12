# 重置操作

## 任务
1. 创建一个临时文件 temp.txt
2. 使用 reset --soft 撤销提交但保留更改
3. 使用 reset --hard 完全丢弃更改

## 验证
```bash
[ ! -f temp.txt ] && echo "Reset successful"
```
