1. `git checkout main`
   `echo "main change" > README.md`
   `git commit -am "Update README on main"`
2. `git checkout -b feature`
   `echo "feature change" > README.md`
   `git commit -am "Update README on feature"`
3. `git checkout main`
   `git merge feature`
   # 手动解决冲突后
   `git add README.md`
   `git commit`
