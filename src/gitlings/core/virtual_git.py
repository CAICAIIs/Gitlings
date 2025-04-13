from typing import Dict, List, Optional
import random
import textwrap
from datetime import datetime, timedelta

class VirtualGit:
    def __init__(self):
        self._state = {
            'repo_initialized': False,
            'branches': ['main'],
            'current_branch': 'main',
            'staged_files': [],
            'working_dir': {},
            'commits': [],
            'remotes': {},
            'tags': {},
            'stashes': [],
            'conflict': False
        }
        self._commit_hash_length = 7
        self._init_sample_data()

    def _init_sample_data(self):
        """初始化一些示例数据使输出更真实"""
        if not self._state['repo_initialized']:
            return
            
        # 添加示例远程仓库
        self._state['remotes']['origin'] = {
            'url': 'https://github.com/example/repo.git',
            'branches': ['main', 'develop']
        }
        
        # 添加一些示例文件
        self._state['working_dir'] = {
            'README.md': 'Sample content',
            'src/main.py': 'print("Hello")',
            '.gitignore': '*.log\n__pycache__/'
        }

    def run_command(self, command: str) -> str:
        """执行模拟的git命令"""
        cmd_parts = command.strip().split()
        if not cmd_parts:
            return ""
            
        # 提取主命令和子命令
        main_cmd = cmd_parts[0]
        if main_cmd != "git":
            return f"git: '{main_cmd}' is not a git command."
            
        if len(cmd_parts) < 2:
            return "usage: git <command> [<args>]"
            
        sub_cmd = cmd_parts[1]
        args = cmd_parts[2:]
        
        # 路由到对应的命令处理函数
        cmd_handlers = {
            # 初始化/克隆
            'init': self._cmd_init,
            'clone': self._cmd_clone,
            # 分支操作
            'branch': self._cmd_branch,
            'checkout': self._cmd_checkout,
            'merge': self._cmd_merge,
            # 远程操作
            'remote': self._cmd_remote,
            'push': self._cmd_push,
            'pull': self._cmd_pull,
            'fetch': self._cmd_fetch,
            # 提交与日志
            'add': self._cmd_add,
            'commit': self._cmd_commit,
            'log': self._cmd_log,
            'status': self._cmd_status,
            # 撤销与回退
            'reset': self._cmd_reset,
            'revert': self._cmd_revert,
            # 标签管理
            'tag': self._cmd_tag,
            # 高级命令
            'rebase': self._cmd_rebase,
            'stash': self._cmd_stash,
            'cherry-pick': self._cmd_cherry_pick,
        }
        
        handler = cmd_handlers.get(sub_cmd)
        if handler:
            return handler(args)
        else:
            return f"git: '{sub_cmd}' is not a simulated command."

    # ---- 初始化/克隆命令 ----
    def _cmd_init(self, args) -> str:
        if self._state['repo_initialized']:
            return "Reinitialized existing Git repository in .git/"
        self._state['repo_initialized'] = True
        self._init_sample_data()
        return "Initialized empty Git repository in .git/"

    def _cmd_clone(self, args) -> str:
        if not args:
            return "fatal: You must specify a repository to clone."
        url = args[0]
        repo_name = url.split('/')[-1].replace('.git', '')
        return f"Cloning into '{repo_name}'...\nremote: Enumerating objects: 100, done.\nReceiving objects: 100% (100/100), 1.23 MiB | 2.56 MiB/s, done."

    # ---- 分支操作命令 ----
    def _cmd_branch(self, args) -> str:
        if not args:
            # 列出所有分支
            branches = []
            for branch in self._state['branches']:
                prefix = '*' if branch == self._state['current_branch'] else ' '
                branches.append(f"{prefix} {branch}")
            return "\n".join(branches)
        
        if args[0] == '-d':
            # 删除分支
            branch = args[1]
            if branch == self._state['current_branch']:
                return f"error: Cannot delete branch '{branch}' checked out at '...'"
            if branch not in self._state['branches']:
                return f"error: branch '{branch}' not found."
            self._state['branches'].remove(branch)
            return f"Deleted branch {branch}."
        elif args[0] == '-D':
            # 强制删除分支
            branch = args[1]
            self._state['branches'].remove(branch)
            return f"Deleted branch {branch} (forced)."
        else:
            # 创建新分支
            new_branch = args[0]
            if new_branch in self._state['branches']:
                return f"fatal: A branch named '{new_branch}' already exists."
            self._state['branches'].append(new_branch)
            return f"Created new branch '{new_branch}'."

    def _cmd_checkout(self, args) -> str:
        if not args:
            return "error: pathspec is required for checkout command."
            
        if args[0] == '-b':
            # 创建并切换分支
            if len(args) < 2:
                return "fatal: branch name required"
            new_branch = args[1]
            if new_branch in self._state['branches']:
                return f"fatal: A branch named '{new_branch}' already exists."
            self._state['branches'].append(new_branch)
            self._state['current_branch'] = new_branch
            return f"Switched to a new branch '{new_branch}'"
        else:
            # 切换分支
            branch = args[0]
            if branch not in self._state['branches']:
                return f"error: pathspec '{branch}' did not match any file(s) known to git."
            self._state['current_branch'] = branch
            return f"Switched to branch '{branch}'"

    def _cmd_merge(self, args) -> str:
        if not args:
            return "fatal: branch name required for merge"
            
        branch = args[0]
        if branch not in self._state['branches']:
            return f"fatal: branch '{branch}' not found."
            
        if self._state['conflict']:
            return "error: Merging is not possible because you have unmerged files."
            
        if '--abort' in args:
            return "Merge aborted."
            
        if '--no-ff' in args:
            # 模拟非快进合并
            commit_hash = self._generate_commit_hash()
            merge_msg = f"Merge branch '{branch}' into {self._state['current_branch']}"
            self._state['commits'].append({
                'hash': commit_hash,
                'message': merge_msg,
                'branch': self._state['current_branch'],
                'is_merge': True
            })
            return f"Merge made by the 'ort' strategy.\n 1 file changed, 1 insertion(+)"
        else:
            # 模拟快进合并
            return f"Updating abc123..def456\nFast-forward"

    # ---- 远程操作命令 ----
    def _cmd_remote(self, args) -> str:
        if not args:
            remotes = []
            for name, data in self._state['remotes'].items():
                remotes.append(f"{name}\t{data['url']} (fetch)")
                remotes.append(f"{name}\t{data['url']} (push)")
            return "\n".join(remotes)
            
        if args[0] == 'add':
            if len(args) < 3:
                return "usage: git remote add <name> <url>"
            name = args[1]
            url = args[2]
            self._state['remotes'][name] = {'url': url, 'branches': []}
            return ""
        elif args[0] == '-v':
            remotes = []
            for name, data in self._state['remotes'].items():
                remotes.append(f"{name}\t{data['url']} (fetch)")
                remotes.append(f"{name}\t{data['url']} (push)")
            return "\n".join(remotes)
        else:
            return f"git remote: '{args[0]}' is not a valid subcommand."

    def _cmd_push(self, args) -> str:
        if not self._state['remotes']:
            return "fatal: No configured push destination."
            
        remote = 'origin'
        branch = self._state['current_branch']
        
        if '-u' in args:
            idx = args.index('-u')
            if len(args) > idx + 2:
                remote = args[idx+1]
                branch = args[idx+2]
            return f"Branch '{branch}' set up to track remote branch '{branch}' from '{remote}'."
        elif '--force' in args or '-f' in args:
            return f" + {branch} -> {branch} (forced update)"
        else:
            return f"Counting objects: 3, done.\nWriting objects: 100% (3/3), 256 bytes | 256.00 KiB/s, done.\nTo github.com:example/repo.git\n   abc123..def456  {branch} -> {branch}"

    def _cmd_pull(self, args) -> str:
        return "remote: Enumerating objects: 5, done.\nremote: Counting objects: 100% (5/5), done.\nMerge made by the 'ort' strategy."

    def _cmd_fetch(self, args) -> str:
        return "remote: Enumerating objects: 5, done.\nremote: Counting objects: 100% (5/5), done."

    # ---- 提交与日志命令 ----
    def _cmd_add(self, args) -> str:
        if not args:
            return "Nothing specified, nothing added."
            
        if args[0] == '.':
            # 暂存所有更改
            for file in self._state['working_dir']:
                if file not in self._state['staged_files']:
                    self._state['staged_files'].append(file)
            return ""
        else:
            # 暂存指定文件
            for file in args:
                if file in self._state['working_dir'] and file not in self._state['staged_files']:
                    self._state['staged_files'].append(file)
            return ""

    def _cmd_commit(self, args) -> str:
        if not self._state['staged_files']:
            return "nothing to commit, working tree clean"
            
        message = "Update files"
        if '-m' in args:
            idx = args.index('-m')
            if len(args) > idx + 1:
                message = args[idx+1]
                
        commit_hash = self._generate_commit_hash()
        self._state['commits'].append({
            'hash': commit_hash,
            'message': message,
            'files': self._state['staged_files'].copy(),
            'branch': self._state['current_branch'],
            'timestamp': datetime.now()
        })
        self._state['staged_files'] = []
        
        changed = len(self._state['commits'][-1]['files'])
        return f"[{self._state['current_branch']} {commit_hash}] {message}\n {changed} files changed"

    def _cmd_log(self, args) -> str:
        if not self._state['commits']:
            return "fatal: your current branch 'main' does not have any commits yet"
            
        log_entries = []
        for commit in reversed(self._state['commits']):
            time_str = commit['timestamp'].strftime("%a %b %d %H:%M:%S %Y")
            entry = f"commit {commit['hash']}\nAuthor: User <user@example.com>\nDate:   {time_str}\n\n    {commit['message']}"
            log_entries.append(entry)
            
        if '--oneline' in args:
            return "\n".join([
                f"{c['hash'][:7]} {c['message']}" 
                for c in reversed(self._state['commits'])
            ])
        return "\n\n".join(log_entries)

    def _cmd_status(self, args) -> str:
        if not self._state['repo_initialized']:
            return "fatal: not a git repository (or any of the parent directories)"
            
        output = [f"On branch {self._state['current_branch']}"]
        
        # 暂存区状态
        if self._state['staged_files']:
            output.append("Changes to be committed:")
            output.append('  (use "git restore --staged <file>..." to unstage)')
            output.extend(f"\tnew file:   {f}" for f in self._state['staged_files'])
        
        # 工作区状态
        unstaged = [
            f for f in self._state['working_dir'] 
            if f not in self._state['staged_files']
        ]
        if unstaged:
            output.append("\nChanges not staged for commit:")
            output.append('  (use "git add <file>..." to update what will be committed)')
            output.extend(f"\tmodified:   {f}" for f in unstaged)
        
        # 未跟踪文件
        untracked = [
            f for f in self._state['working_dir'] 
            if f not in self._state['staged_files'] and f not in unstaged
        ]
        if untracked:
            output.append("\nUntracked files:")
            output.append('  (use "git add <file>..." to include in what will be committed)')
            output.extend(f"\t{f}" for f in untracked)
        
        return "\n".join(output)

    # ---- 撤销与回退命令 ----
    def _cmd_reset(self, args) -> str:
        if not args:
            return "fatal: option required"
            
        if args[0] == '--hard':
            if len(args) > 1 and args[1] == 'HEAD~1':
                if len(self._state['commits']) > 0:
                    self._state['commits'].pop()
                    return "HEAD is now at abc123 Previous commit message"
            return "HEAD is now at abc123"
        elif args[0] == '--soft':
            return "Reset to previous commit (changes staged)"
        else:
            return f"git reset: '{args[0]}' is not a valid option"

    def _cmd_revert(self, args) -> str:
        if not args:
            return "fatal: commit id required"
            
        commit_id = args[0]
        return f"[{self._state['current_branch']} abc123] Revert \"{commit_id}\"\n 1 file changed, 1 deletion(-)"

    # ---- 标签管理命令 ----
    def _cmd_tag(self, args) -> str:
        if not args:
            return "\n".join(self._state['tags'].keys())
            
        tag_name = args[0]
        self._state['tags'][tag_name] = {
            'commit': self._get_latest_commit_hash(),
            'timestamp': datetime.now()
        }
        return f"Created tag '{tag_name}'"

    # ---- 高级命令 ----
    def _cmd_rebase(self, args) -> str:
        if not args:
            return "fatal: branch name required for rebase"
            
        if '--abort' in args:
            return "Rebase aborted."
            
        if '--continue' in args:
            return "Successfully rebased and updated refs/heads/main."
            
        if '-i' in args:
            return textwrap.dedent("""
            pick abc123 First commit
            pick def456 Second commit
            
            # Rebase xyz789 onto abc123 (2 commands)
            #
            # Commands:
            # p, pick <commit> = use commit
            # r, reword <commit> = use commit, but edit the commit message
            # e, edit <commit> = use commit, but stop for amending
            # s, squash <commit> = use commit, but meld into previous commit
            # f, fixup <commit> = like "squash", but discard this commit's log message
            # x, exec <command> = run command (the rest of the line) using shell
            # b, break = stop here (continue rebase later with 'git rebase --continue')
            # d, drop <commit> = remove commit
            # l, label <label> = label current HEAD with a name
            # t, reset <label> = reset HEAD to a label
            # m, merge [-C <commit> | -c <commit>] <label> [# <oneline>]
            """)
            
        branch = args[0]
        return f"Successfully rebased and updated refs/heads/{branch}."

    def _cmd_stash(self, args) -> str:
        if not args:
            # 默认stash save
            stash_id = f"stash@{{{len(self._state['stashes'])}}}"
            self._state['stashes'].append({
                'id': stash_id,
                'branch': self._state['current_branch'],
                'files': self._state['working_dir'].keys()
            })
            return f"Saved working directory and index state WIP on {self._state['current_branch']}: abc123 Commit message"
            
        if args[0] == 'list':
            return "\n".join([
                f"{s['id']}: WIP on {s['branch']}: abc123 Commit message" 
                for s in self._state['stashes']
            ])
        elif args[0] == 'apply':
            return "On branch main\nChanges not staged for commit:\n\tmodified:   file.txt"
        elif args[0] == 'drop':
            return "Dropped refs/stash@{0}"
        else:
            return f"git stash: '{args[0]}' is not a valid subcommand"

    def _cmd_cherry_pick(self, args) -> str:
        if not args:
            return "fatal: commit id required"
            
        commit_id = args[0]
        return f"[{self._state['current_branch']} abc123] {commit_id}\n 1 file changed, 1 insertion(+)"

    # ---- 辅助方法 ----
    def _generate_commit_hash(self) -> str:
        """生成随机的commit hash"""
        import random
        import string
        return ''.join(random.choices('0123456789abcdef', k=self._commit_hash_length))

    def _get_latest_commit_hash(self) -> str:
        """获取最新的commit hash"""
        if self._state['commits']:
            return self._state['commits'][-1]['hash']
        return '0' * self._commit_hash_length

    # ---- 暂未实现的命令 ----
    def _cmd_diff(self, args) -> str:
        pass
        
    def _cmd_config(self, args) -> str:
        pass
        
    def _cmd_show(self, args) -> str:
        pass
        
    def _cmd_blame(self, args) -> str:
        pass
        
    def _cmd_submodule(self, args) -> str:
        pass
