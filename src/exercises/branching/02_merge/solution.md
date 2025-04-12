1. `git checkout -b feature`
   `echo "feature" > feature.txt`
   `git add feature.txt`
   `git commit -m "Add feature"`
2. `git checkout main`
3. `git merge feature --no-ff -m "Merge feature branch"`
