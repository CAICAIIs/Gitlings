1. `git checkout main`
   `echo "base" > base.txt`
   `git add base.txt`
   `git commit -m "Base commit"`
2. `git checkout -b feature`
   `echo "feature" > feature.txt`
   `git add feature.txt`
   `git commit -m "Feature commit"`
3. `git rebase main`
