# 常见问题

## 远程仓库

1.   本地已建仓库再与 GitHub 上仓库进行连接后，进行上传后报错：

```sh
$ git push --set-upstream ts main
To https://github.com/Soiya-g/testRep.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/Soiya-g/testRep.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

>   原因：
>
>   因为 Git 检测到你要合并的两个分支有**不相关的历史**，这是一种安全保护机制。
>
>   通常发生在：
>
>   -   本地初始化了新仓库，但远程仓库已有其他历史
>   -   两个完全独立开始的代码库
>   -   克隆不完整或历史记录损坏
>
>   解决方法：
>
>   允许合并不相关历史
>
>   ```sh
>   git merge ts/main --allow-unrelated-histories
>   ```

2.   本地仓库与远程仓库连接后，无法进行推送，报错

```sh
$ git push --set-upstream ts main
error: src refspec main does not match any
error: failed to push some refs to 'https://github.com/Soiya-g/testRep.git'
```

>原因：
>
>进行拉取未合并
>
>解决方法
>
>```sh
>git log --oneline ts/main
>git log --oneline main
>git merge ts/mian
>```

3.   首次进行推送，报错

```sh
$ git push
fatal: The current branch master has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream ts master

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.
```

>   原因：
>
>   当前的本地分支 `master` 还没有设置对应的上游分支（upstream branch）
>
>   上游分支就是告诉 Git：
>
>   -   这个本地分支应该推送到**哪个远程仓库**
>   -   应该推送到远程的**哪个分支**
>   -   从哪个远程分支**拉取更新**
>
>   解决方案：
>
>   ```sh
>   git push --set-upstream ts master
>   ```

4.   本地分支与远程分支名不一致，自动会在远程仓库建立新的分支。

>   解决方案：
>
>   1.   更改本地分支名后推送
>
>   ```sh
>   git branch -m master main
>   git push --set-upstream ts main
>   ```
>
>   2.   本地分支 master 推送到远程 main
>
>   ```sh
>   git push --set-upstream ts master:main
>   ```

