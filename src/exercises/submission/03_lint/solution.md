1. `npm init -y`
   `npm install --save-dev @commitlint/cli @commitlint/config-conventional husky`
2. `echo "module.exports = {extends: ['@commitlint/config-conventional']}" > commitlint.config.js`
3. `npx husky install`
   `npx husky add .husky/commit-msg 'npx commitlint --edit "$1"'`
