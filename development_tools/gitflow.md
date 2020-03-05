# git工作流

## 一、集中式工作流

但使用`Git`加强开发的工作流，相比`SVN`，`Git`有以下两个优势: 首先，每个开发者可以有属于自己的整个工程的本地拷贝。隔离的环境让各个开发者的工作和项目的其他部分修改独立开来 —— 即自由地提交到自己的本地仓库，先完全忽略上游的开发，直到方便的时候再把修改反馈上去。

### 1.1 工作方式

像`Subversion`一样，集中式工作流以中央仓库作为项目所有修改的单点实体。相比`SVN`缺省的开发分支`trunk`，`Git`叫做`master`，所有修改提交到这个分支上。本工作流只用到`master`这一个分支。

首先，开发者克隆中央仓库。在自己的项目拷贝中，像`SVN`一样的编辑文件和提交修改；但修改是存在本地的，和中央仓库是完全隔离的。开发者可以把和上游的同步延后到一个方便时间点。

然后，开发者发布修改到正式项目中，开发者要把本地`master`分支的修改『推』到中央仓库中。这相当于`svn commit`操作，但`push`操作会把所有还不在中央仓库的本地提交都推上去。

![image-20200226171301103](../../image/image-20200226171301103.png)

### 1.2 冲突解决

中央仓库代表了正式项目，所以提交历史应该被尊重且是稳定不变的。如果开发者本地的提交历史和中央仓库有分歧，`Git`会拒绝`push`提交否则会覆盖已经在中央库的正式提交。

![image-20200226171417409](../../image/image-20200226171417409.png)

在开发者提交自己功能修改到中央库前，需要先`fetch`在中央库的新增提交，`rebase`自己提交到中央库提交历史之上。 这样做的意思是在说，『我要把自己的修改加到别人已经完成的修改上。』最终的结果是一个完美的线性历史，就像以前的`SVN`的工作流中一样。 

如果本地修改和上游提交有冲突，`Git`会暂停`rebase`过程，给你手动解决冲突的机会。`Git`解决合并冲突，用和生成提交一样的[`git status`](https://www.atlassian.com/git/tutorial/git-basics#!status)和[`git add`](https://www.atlassian.com/git/tutorial/git-basics#!add)命令，很一致方便。还有一点，如果解决冲突时遇到麻烦，`Git`可以很简单中止整个`rebase`操作，重来一次（或者让别人来帮助解决）。

`rebase`分为多个场景：

- 在修改的代码未push到远程仓库时，这时`rebase`会将线上的变更先同步到本地仓库，push之后出现冲突后在本地解决即可,若不先进行`git pull --rebase`,如果`push`的代码多人进行修改后会直接出现冲突，无法正常提交，这时还是需要进行`git pull --rebase`,所以在`push`之前需要先`rebase`

### 1.3 示例

让我们一起逐步分解来看看一个常见的小团队如何用这个工作流来协作的。有两个开发者小明和小红，看他们是如何开发自己的功能并提交到中央仓库上的。

第一步，有人在服务器上创建好中央仓库。如果是新项目，你可以初始化一个空仓库；否则你要导入已有的`Git`或`SVN`仓库。

中央仓库应该是个裸仓库（`bare repository`），即没有工作目录（`working directory`）的仓库。可以用下面的命令创建：

```
ssh user@host
git init --bare /path/to/repo.git
```

确保写上有效的`user`（`SSH`的用户名），`host`（服务器的域名或IP地址），`/path/to/repo.git`（你想存放仓库的位置）。 注意，为了表示是一个裸仓库，按照约定加上`.git`扩展名到仓库名上。

#### 所有人克隆仓库

下一步，各个开发者创建整个项目的本地拷贝。通过[`git clone`](https://www.atlassian.com/git/tutorial/git-basics#!clone)命令完成：

```
git clone ssh://user@host/path/to/repo.git
```

基于你后续会持续和克隆的仓库做交互的假设，克隆仓库时`Git`会自动添加远程别名`origin`指回『父』仓库。

#### 小明开发功能

在小明的本地仓库中，他使用标准的`Git`过程开发功能：编辑、暂存（`Stage`）和提交。 如果你不熟悉暂存区（`Staging Area`），这里说明一下：**暂存区**用来准备一个提交，但可以不用把工作目录中所有的修改内容都包含进来。 这样你可以创建一个高度聚焦的提交，尽管你本地修改很多内容。

```
git status # 查看本地仓库的修改状态
git add # 暂存文件
git commit # 提交文件
```

请记住，因为这些命令生成的是本地提交，小明可以按自己需求反复操作多次，而不用担心中央仓库上有了什么操作。 对需要多个更简单更原子分块的大功能，这个做法是很有用的。

#### 小红开发功能

与此同时，小红在自己的本地仓库中用相同的编辑、暂存和提交过程开发功能。和小明一样，她也不关心中央仓库有没有新提交； 当然更不关心小明在他的本地仓库中的操作，因为所有本地仓库都是私有的。

#### 小明发布功能

一旦小明完成了他的功能开发，会发布他的本地提交到中央仓库中，这样其它团队成员可以看到他的修改。他可以用下面的[`git push`命令](https://www.atlassian.com/git/tutorial/remote-repositories#!push)：

```
git push origin master
```

注意，`origin`是在小明克隆仓库时`Git`创建的远程中央仓库别名。`master`参数告诉`Git`推送的分支。 由于中央仓库自从小明克隆以来还没有被更新过，所以`push`操作不会有冲突，成功完成。

#### 小红试着发布功能

一起来看看在小明发布修改后，小红`push`修改会怎么样？她使用完全一样的`push`命令：

```
git push origin master
```

但她的本地历史已经和中央仓库有分岐了，`Git`拒绝操作并给出下面很长的出错消息：

```
error: failed to push some refs to '/path/to/repo.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Merge the remote changes (e.g. 'git pull')
hint: before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

这避免了小红覆写正式的提交。她要先`pull`小明的更新到她的本地仓库合并上她的本地修改后，再重试。

#### 小红在小明的提交之上`rebase`

小红用[`git pull`](https://www.atlassian.com/git/tutorial/remote-repositories#!pull)合并上游的修改到自己的仓库中。 这条命令类似`svn update`——拉取所有上游提交命令到小红的本地仓库，并尝试和她的本地修改合并：

```
git pull --rebase origin master
```

`--rebase`选项告诉`Git`把小红的提交移到同步了中央仓库修改后的`master`分支的顶部，如下图所示：

![image-20200226173135094](../../image/image-20200226173135094.png)

如果你忘加了这个选项，`pull`操作仍然可以完成，但每次`pull`操作要同步中央仓库中别人修改时，提交历史会以一个多余的『合并提交』结尾。 对于集中式工作流，最好是使用`rebase`而不是生成一个合并提交。用`rebase`后相当于只有最初的一次`push`提交（**待确认**）

#### 小红解决合并冲突

`rebase`操作过程是把本地提交一次一个地迁移到更新了的中央仓库`master`分支之上。 这意味着可能要解决在迁移某个提交时出现的合并冲突，而不是解决包含了所有提交的大型合并时所出现的冲突。 这样的方式让你尽可能保持每个提交的聚焦和项目历史的整洁。反过来，简化了哪里引入`Bug`的分析，如果有必要，回滚修改也可以做到对项目影响最小。

如果小红和小明的功能是不相关的，不大可能在`rebase`过程中有冲突。如果有，`Git`在合并有冲突的提交处暂停`rebase`过程，输出下面的信息并带上相关的指令：

```
CONFLICT (content): Merge conflict in <some-file>
```

![image-20200226173516598](../../image/image-20200226173516598.png)

`Git`很赞的一点是，任何人可以解决他自己的冲突。在这个例子中，小红可以简单的运行[`git status`](https://www.atlassian.com/git/tutorial/git-basics#!status)命令来查看哪里有问题。 冲突文件列在`Unmerged paths`（未合并路径）一节中：

```
# Unmerged paths:
# (use "git reset HEAD <some-file>..." to unstage)
# (use "git add/rm <some-file>..." as appropriate to mark resolution)
#
# both modified: <some-file>
```

接着小红编辑这些文件。修改完成后，用老套路暂存这些文件，并让[`git rebase`](https://www.atlassian.com/git/tutorial/rewriting-git-history#!rebase)完成剩下的事：

```
git add <some-file> 
git rebase --continue
```

要做的就这些了。`Git`会继续一个一个地合并后面的提交，如其它的提交有冲突就重复这个过程。

如果你碰到了冲突，但发现搞不定，不要惊慌。只要执行下面这条命令，就可以回到你执行[`git pull --rebase`](https://www.atlassian.com/git/tutorial/remote-repositories#!pull)命令前的样子：

```
git rebase --abort
```

#### 小红成功发布功能

小红完成和中央仓库的同步后，就能成功发布她的修改了：

```
git push origin master
```

如你所见，仅使用几个`Git`命令我们就可以模拟出传统`Subversion`开发环境。对于要从`SVN`迁移过来的团队来说这太好了，但没有发挥出`Git`分布式本质的优势。

如果你的团队适应了集中式工作流，但想要更流畅的协作效果，绝对值得探索一下 `功能分支工作流` 的收益。 通过为一个功能分配一个专门的分支，能够做到一个新增功能集成到正式项目之前对新功能进行深入讨论。

#### `问题`

- 如果在修改未`add`的时候进行`rebase`会出现什么问题？
- 在修改`add`或者`stage`之后`rebase`会出现什么问题？



## 二、功能分支工作流

功能分支工作流以集中式工作流为基础，不同的是为各个新功能分配一个专门的分支来开发。这样可以在把新功能集成到正式项目前，用`Pull Requests`的方式讨论变更。

![image-20200226180626922](../../image/image-20200226180626922.png)

一旦你玩转了[集中式工作流](https://github.com/xirong/my-git/blob/master/workflow-centralized.md)，在开发过程中可以很简单地加上功能分支，用来鼓励开发者之间协作和简化交流。

功能分支工作流背后的核心思路是所有的功能开发应该在一个专门的分支，而不是在`master`分支上。 这个隔离可以方便多个开发者在各自的功能上开发而不会弄乱主干代码。 另外，也保证了`master`分支的代码一定不会是有问题的，极大有利于集成环境。

功能开发隔离也让[`pull requests`工作流](https://github.com/xirong/my-git/blob/master/pull-request.md)成功可能， `pull requests`工作流能为每个分支发起一个讨论，在分支合入正式项目之前，给其它开发者有表示赞同的机会。 另外，如果你在功能开发中有问题卡住了，可以开一个`pull requests`来向同学们征求建议。 这些做法的重点就是，`pull requests`让团队成员之间互相评论工作变成非常方便！

### 2.1 工作方式

功能分支工作流仍然用中央仓库，并且`master`分支还是代表了正式项目的历史。 但不是直接提交本地历史到各自的本地`master`分支，开发者每次在开始新功能前先创建一个新分支。 功能分支应该有个有描述性的名字，比如`animated-menu-items`或`issue-#1061`，这样可以让分支有个清楚且高聚焦的用途。

对于`master`分支和功能分支，`Git`是没有技术上的区别，所以开发者可以用和集中式工作流中完全一样的方式编辑、暂存和提交修改到功能分支上。

另外，功能分支也可以（且应该）`push`到中央仓库中。这样不修改正式代码就可以和其它开发者分享提交的功能。 由于`master`是仅有的一个『特殊』分支，在中央仓库上存多个功能分支不会有任何问题。当然，这样做也可以很方便地备份各自的本地提交。

### 2.2 `Pull` `Request`

功能分支除了可以隔离功能的开发，也使得通过[`Pull Requests`](https://github.com/xirong/my-git/blob/master/pull-request.md)讨论变更成为可能。 一旦某个开发者完成一个功能，不是立即合并到`master`，而是`push`到中央仓库的功能分支上并发起一个`Pull Request`请求，将修改合并到`master`。 在修改成为主干代码前，这让其它的开发者有机会先去`Review`变更。

`Code Review`是`Pull Requests`的一个重要的收益，而`Pull Requests`则是讨论代码的一个通用方式。 你可以把`Pull Requests`作为专门给某个分支的讨论。这意味着可以在更早的开发过程中就可以进行`Code Review`。 比如，一个开发者开发功能需要帮助时，要做的就是发起一个`Pull Request`，相关的人就会自动收到通知，在相关的提交旁边能看到需要帮助解决的问题。

一旦`Pull Request`被接受了，发布功能要做的就和集中式工作流就很像了。 首先，确定本地的`master`分支和上游的`master`分支是同步的。然后合并功能分支到本地`master`分支并`push`已经更新的本地`master`分支到中央仓库。

仓库管理的产品解决方案像[`Bitbucket`](http://bitbucket.org/)或[`Stash`](http://www.atlassian.com/stash)，可以良好地支持`Pull Requests`。可以看看`Stash`的[`Pull Requests`文档](https://confluence.atlassian.com/display/STASH/Using+pull+requests+in+Stash)。

### 2.3 示例

下面的示例演示了如何把`Pull Requests`作为`Code Review`的方式，但注意`Pull Requests`可以用于很多其它的目的。

#### 小红开始开发一个新功能

![image-20200226195430062](../../image/image-20200226195430062.png)

在开始开发功能前，小红需要一个独立的分支。使用下面的命令[新建一个分支](https://www.atlassian.com/git/tutorial/git-branches#!checkout)：

```
git checkout -b marys-feature master
```

这个命令建出一个基于`master`名为`marys-feature`的分支，`Git`的`-b`选项表示如果分支还不存在则新建分支。 这个新分支上，小红按老套路编辑、暂存和提交修改，按需要提交以实现功能：

```
git status
git add <some-file>
git commit
```

#### 小红要去吃个午饭

早上小红为新功能添加一些提交。 去吃午饭前，`push`功能分支到中央仓库是很好的做法，这样可以方便地备份，如果和其它开发协作，也让他们可以看到小红的提交。

```
git push -u origin marys-feature
```

这条命令`push` `marys-feature`分支到中央仓库（`origin`），`-u`选项设置本地分支去跟踪远程对应的分支。 设置好跟踪的分支后，小红就可以使用`git push`命令省去指定推送分支的参数。

#### 小红完成功能开发

小红吃完午饭回来，完成整个功能的开发。[在合并到`master`之前](https://www.atlassian.com/git/tutorial/git-branches#!merge)， 她发起一个`Pull Request`让团队的其它人知道功能已经完成。但首先，她要确认中央仓库中已经有她最近的提交：

```
git push
```

然后，在她的`Git` `GUI`客户端中发起`Pull Request`，请求合并`marys-feature`到`master`，团队成员会自动收到通知。 `Pull Request`很酷的是可以在相关的提交旁边显示评注，所以你可以对某个变更集提问。

#### 小黑收到`Pull Request`

小黑收到了`Pull Request`后会查看`marys-feature`的修改。决定在合并到正式项目前是否要做些修改，且通过`Pull Request`和小红来回地讨论。

#### 小红再做修改

要再做修改，小红用和功能第一个迭代完全一样的过程。编辑、暂存、提交并`push`更新到中央仓库。小红这些活动都会显示在`Pull Request`上，小黑可以断续做评注。

如果小黑有需要，也可以把`marys-feature`分支拉到本地，自己来修改，他加的提交也会一样显示在`Pull Request`上。

#### 小红发布她的功能

一旦小黑可以的接受`Pull Request`，就可以合并功能到稳定项目代码中（可以由小黑或是小红来做这个操作）：

```
git checkout master
git pull
git pull origin marys-feature
git push
```

无论谁来做合并，首先要检出`master`分支并确认是它是最新的。然后执行`git pull origin marys-feature`合并`marys-feature`分支到和已经和远程一致的本地`master`分支。 你可以使用简单`git merge marys-feature`命令，但前面的命令可以保证总是最新的新功能分支。 最后更新的`master`分支要重新`push`回到`origin`。

这个过程常常会生成一个合并提交。有些开发者喜欢有合并提交，因为它像一个新功能和原来代码基线的连通符。 但如果你偏爱线性的提交历史，可以在执行合并时`rebase`新功能到`master`分支的顶部，这样生成一个快进（`fast-forward`）的合并。

一些`GUI`客户端可以只要点一下『接受』按钮执行好上面的命令来自动化`Pull Request`接受过程。 如果你的不能这样，至少在功能合并到`master`分支后能自动关闭`Pull Request`。

#### 与此同时，小明在做和小红一样的事

当小红和小黑在`marys-feature`上工作并讨论她的`Pull Request`的时候，小明在自己的功能分支上做完全一样的事。

通过隔离功能到独立的分支上，每个人都可以自主的工作，当然必要的时候在开发者之间分享变更还是比较繁琐的。

到了这里，但愿你发现了功能分支可以很直接地在 `集中式工作流` 的仅有的`master`分支上完成多功能的开发。 另外，功能分支还使用了`Pull Request`，使得可以在你的版本控制`GUI`客户端中讨论某个提交。

功能分支工作流是开发项目异常灵活的方式。问题是，有时候太灵活了。对于大型团队，常常需要给不同分支分配一个更具体的角色。 `Gitflow`工作流是管理功能开发、发布准备和维护的常用模式。

## 三、Gitflow工作流

`Gitflow`工作流通过为功能开发、发布准备和维护分配独立的分支，让发布迭代过程更流畅。严格的分支模型也为大型项目提供了一些非常必要的结构。

![image-20200226201101141](../../image/image-20200226201101141.png)

这节介绍的[`Gitflow`工作流](http://nvie.com/posts/a-successful-git-branching-model/)借鉴自在[nvie](http://nvie.com/)的*Vincent Driessen*。

`Gitflow`工作流定义了一个围绕项目发布的严格分支模型。虽然比[功能分支工作流](https://github.com/xirong/my-git/blob/master/workflow-feature-branch.md)复杂几分，但提供了用于一个健壮的用于管理大型项目的框架。

`Gitflow`工作流没有用超出功能分支工作流的概念和命令，而是为不同的分支分配一个明确的角色，并定义分支之间如何和什么时候进行交互。 除了使用功能分支，在做准备、维护和记录发布时，也定义了各自的分支。 当然你可以用上功能分支工作流所有的好处：`Pull Requests`、隔离实验性开发和更高效的协作。

### 3.1 工作方式

`Gitflow`工作流仍然用中央仓库作为所有开发者的交互中心。和其它的工作流一样，开发者在本地工作并`push`分支到要中央仓库中。

### 3.2 历史分支

相对于使用仅有的一个`master`分支，`Gitflow`工作流使用两个分支来记录项目的历史。`master`分支存储了正式发布的历史，而`develop`分支作为功能的集成分支。 这样也方便`master`分支上的所有提交分配一个版本号。

![image-20200226201242827](../../image/image-20200226201242827.png)

### 3.3 功能分支

每个新功能位于一个自己的分支，这样可以[`push`到中央仓库以备份和协作](https://www.atlassian.com/git/tutorial/remote-repositories#!push)。 但功能分支不是从`master`分支上拉出新分支，而是使用`develop`分支作为父分支。当新功能完成时，[合并回`develop`分支](https://www.atlassian.com/git/tutorial/git-branches#!merge)。 新功能提交应该从不直接与`master`分支交互。

![image-20200226201336568](../../image/image-20200226201336568.png)

注意，从各种含义和目的上来看，功能分支加上`develop`分支就是功能分支工作流的用法。但`Gitflow`工作流没有在这里止步。

### 3.4 发布分支

![image-20200226201412729](../../image/image-20200226201412729.png)

一旦`develop`分支上有了做一次发布（或者说快到了既定的发布日）的足够功能，就从`develop`分支上`checkout`一个发布分支。 新建的分支用于开始发布循环，所以从这个时间点开始之后新的功能不能再加到这个分支上—— **这个分支只应该做`Bug`修复**、**文档生成和其它面向发布任务**。 一旦对外发布的工作都完成了，**发布分支合并到`master`分支并分配一个版本号打好`Tag`**。 另外，**这些从新建发布分支以来的做的修改要合并回`develop`分支。**

使用一个用于发布准备的专门分支，使得一个团队可以在完善当前的发布版本的同时，另一个团队可以继续开发下个版本的功能。 这也打造定义良好的开发阶段（比如，可以很轻松地说，『这周我们要做准备发布版本4.0』，并且在仓库的目录结构中可以实际看到）。

常用的分支约定：

```
用于新建发布分支的分支: develop
用于合并的分支: master
分支命名: release-* 或 release/*
```

### 3.5 维护分支

![image-20200226201712168](../../image/image-20200226201712168.png)

维护分支或说是热修复（`hotfix`）分支用于给产品发布版本（`production releases`）快速生成补丁，这是唯一可以直接从`master`分支`fork`出来的分支。 修复完成，修改应该马上合并回`master`分支和`develop`分支（当前的发布分支），`master`分支应该用新的版本号打好`Tag`。

为`Bug`修复使用专门分支，让团队可以处理掉问题而不用打断其它工作或是等待下一个发布循环。 你可以把维护分支想成是一个直接在`master`分支上处理的临时发布。

### 3.6 示例

#### 创建开发分支

![image-20200226201939182](../../image/image-20200226201939182.png)

第一步为`master`分支配套一个`develop`分支。简单来做可以[本地创建一个空的`develop`分支](https://www.atlassian.com/git/tutorial/git-branches#!branch)，`push`到服务器上：

```
git branch develop
git push -u origin develop
```

以后这个分支将会包含了项目的全部历史，而`master`分支将只包含了部分历史。其它开发者这时应该[克隆中央仓库](https://www.atlassian.com/git/tutorial/git-basics#!clone)，建好`develop`分支的跟踪分支：

```
git clone ssh://user@host/path/to/repo.git
# 不使用-b参数会出现什么问题
git checkout -b develop origin/develop
```

现在每个开发都有了这些历史分支的本地拷贝。

#### 小红和小明开始开发新功能

![image-20200226202129292](../../image/image-20200226202129292.png)

这个示例中，小红和小明开始各自的功能开发。他们需要为各自的功能创建相应的分支。新分支不是基于`master`分支，而是应该[基于`develop`分支](https://www.atlassian.com/git/tutorial/git-branches#!checkout)：

```
git checkout -b some-feature develop
```

他们用老套路添加提交到各自功能分支上：编辑、暂存、提交：

```
git status
git add <some-file>
git commit
```

#### 小红完成功能开发

![image-20200226202157382](../../image/image-20200226202157382.png)

添加了提交后，小红觉得她的功能OK了。如果团队使用`Pull Requests`，这时候可以发起一个用于合并到`develop`分支。 否则她可以直接合并到她本地的`develop`分支后`push`到中央仓库：

```
git pull origin develop
git checkout develop
git merge some-feature
git push
git branch -d some-feature
```

第一条命令在合并功能前确保`develop`分支是最新的。注意，功能决不应该直接合并到`master`分支。 冲突解决方法和[集中式工作流](https://github.com/xirong/my-git/blob/master/workflow-centralized.md)一样。

#### 小红开始准备发布

![image-20200226202315536](../../image/image-20200226202315536.png)

这个时候小明正在实现他的功能，小红开始准备她的第一个项目正式发布。 像功能开发一样，她用一个新的分支来做发布准备。这一步也确定了发布的版本号：

```
git checkout -b release-0.1 develop
```

这个分支是清理发布、执行所有测试、更新文档和其它为下个发布做准备操作的地方，像是一个专门用于改善发布的功能分支。

只要小红创建这个分支并`push`到中央仓库，这个发布就是功能冻结的。任何不在`develop`分支中的新功能都推到下个发布循环中。

#### 小红完成发布

![image-20200226202519071](../../image/image-20200226202519071.png)

一旦准备好了对外发布，小红合并修改到`master`分支和`develop`分支上，删除发布分支。合并回`develop`分支很重要，因为在发布分支中已经提交的更新需要在后面的新功能中也要是可用的。 另外，如果小红的团队要求`Code Review`，这是一个发起`Pull Request`的理想时机。

```
git checkout master
git merge release-0.1
git push
git checkout develop
git merge release-0.1
git push
git branch -d release-0.1
```

发布分支是作为功能开发（`develop`分支）和对外发布（`master`分支）间的缓冲。只要有合并到`master`分支，就应该打好`Tag`以方便跟踪。

```
git tag -a 0.1 -m "Initial public release" master
git push --tags
```

`Git`有提供各种勾子（`hook`），即仓库有事件发生时触发执行的脚本。 可以配置一个勾子，在你`push`中央仓库的`master`分支时，自动构建好版本，并对外发布。

#### 最终用户发现`Bug`

![image-20200226202708710](../../image/image-20200226202708710.png)

对外版本发布后，小红小明一起开发下一版本的新功能，直到有最终用户开了一个`Ticket`抱怨当前版本的一个`Bug`。 为了处理`Bug`，小红（或小明）从`master`分支上拉出了一个维护分支，提交修改以解决问题，然后直接合并回`master`分支：

```
git checkout -b issue-#001 master
# Fix the bug
git checkout master
git merge issue-#001
git push
```

就像发布分支，维护分支中新加这些重要修改需要包含到`develop`分支中，所以小红要执行一个合并操作。然后就可以安全地[删除这个分支](https://www.atlassian.com/git/tutorial/git-branches#!branch)了：

```
git checkout develop
git merge issue-#001
git push
git branch -d issue-#001
```

到了这里，但愿你对[集中式工作流](https://github.com/xirong/my-git/blob/master/workflow-centralized.md)、[功能分支工作流](https://github.com/xirong/my-git/blob/master/workflow-feature-branch.md)和`Gitflow`工作流已经感觉很舒适了。 你应该也牢固的掌握了本地仓库的潜能，`push`/`pull`模式和`Git`健壮的分支和合并模型。

记住，这里演示的工作流只是可能用法的例子，而不是在实际工作中使用`Git`不可违逆的条例。 所以不要畏惧按自己需要对工作流的用法做取舍。不变的目标就是让`Git`为你所用。

## 四、Forking工作流

`Forking`工作流是分布式工作流，充分利用了`Git`在分支和克隆上的优势。可以安全可靠地管理大团队的开发者（`developer`），并能接受不信任贡献者（`contributor`）的提交。

`Forking`工作流和前面讨论的几种工作流有根本的不同，这种工作流不是使用单个服务端仓库作为『中央』代码基线，而让各个开发者都有一个服务端仓库。这意味着各个代码贡献者有2个`Git`仓库而不是1个：一个本地私有的，另一个服务端公开的。

![image-20200226202849154](../../image/image-20200226202849154.png)

`Forking`工作流的一个主要优势是，贡献的代码可以被集成，而不需要所有人都能`push`代码到仅有的中央仓库中。 开发者`push`到自己的服务端仓库，而只有项目维护者才能`push`到正式仓库。 这样项目维护者可以接受任何开发者的提交，但无需给他正式代码库的写权限。

效果就是一个分布式的工作流，能为大型、自发性的团队（包括了不受信的第三方）提供灵活的方式来安全的协作。 也让这个工作流成为开源项目的理想工作流。

### 4.1 工作方式

和其它的`Git`工作流一样，`Forking`工作流要先有一个公开的正式仓库存储在服务器上。 但一个新的开发者想要在项目上工作时，不是直接从正式仓库克隆，而是`fork`正式项目在服务器上创建一个拷贝。

这个仓库拷贝作为他个人公开仓库 —— 其它开发者不允许`push`到这个仓库，但可以`pull`到修改（后面我们很快就会看这点很重要）。 在创建了自己服务端拷贝之后，和之前的工作流一样，开发者执行[`git clone`命令](https://www.atlassian.com/git/tutorial/git-basics#!clone)克隆仓库到本地机器上，作为私有的开发环境。

要提交本地修改时，`push`提交到自己公开仓库中 —— 而不是正式仓库中。 然后，给正式仓库发起一个`pull request`，让项目维护者知道有更新已经准备好可以集成了。 对于贡献的代码，`pull request`也可以很方便地作为一个讨论的地方。

为了集成功能到正式代码库，维护者`pull`贡献者的变更到自己的本地仓库中，检查变更以确保不会让项目出错， [合并变更到自己本地的`master`分支](https://www.atlassian.com/git/tutorial/git-branches#!merge)， 然后[`push`](https://www.atlassian.com/git/tutorial/remote-repositories#!push)`master`分支到服务器的正式仓库中。 到此，贡献的提交成为了项目的一部分，其它的开发者应该执行`pull`操作与正式仓库同步自己本地仓库。

### 4.2 正式仓库

在`Forking`工作流中，『官方』仓库的叫法只是一个约定，理解这点很重要。 从技术上来看，各个开发者仓库和正式仓库在`Git`看来没有任何区别。 事实上，让正式仓库之所以正式的唯一原因是它是项目维护者的公开仓库。

### 4.3 `Forking`工作流的分支使用方式

所有的个人公开仓库实际上只是为了方便和其它的开发者共享分支。 各个开发者应该用分支隔离各个功能，就像在[功能分支工作流](https://github.com/xirong/my-git/blob/master/workflow-feature-branch.md)和[`Gitflow`工作流](https://github.com/xirong/my-git/blob/master/workflow-forking.md)一样。 唯一的区别是这些分支被共享了。在`Forking`工作流中这些分支会被`pull`到另一个开发者的本地仓库中，而在功能分支工作流和`Gitflow`工作流中是直接被`push`到正式仓库中。

**个人理解不同开发者相当于不同分支，每个人开发独立的功能，某两个开发者需要合并功能的时候，找到对方的仓库发起`pull` `request`，对于正式仓库也类似，需要从新建分支发起`pull request`**

### 4.4 示例

#### 项目维护者初始化正式仓库

![image-20200305143724888](../../image/image-20200305143724888.png)

和任何使用`Git`项目一样，第一步是创建在服务器上一个正式仓库，让所有团队成员都可以访问到。 通常这个仓库也会作为项目维护者的公开仓库。

[公开仓库应该是裸仓库](https://www.atlassian.com/git/tutorial/git-basics#!init)，不管是不是正式代码库。 所以项目维护者会运行像下面的命令来搭建正式仓库：

```
ssh user@host
git init --bare /path/to/repo.git
```

`Bitbucket`和`Stash`提供了一个方便的`GUI`客户端以完成上面命令行做的事。 这个搭建中央仓库的过程和前面提到的工作流完全一样。 如果有现存的代码库，维护者也要`push`到这个仓库中。

#### 开发者`fork`正式仓库

![image-20200305143736165](../../image/image-20200305143736165.png)

其它所有的开发需要`fork`正式仓库。 可以用`git clone`命令[用`SSH`协议连通到服务器](https://confluence.atlassian.com/display/BITBUCKET/Set+up+SSH+for+Git)， 拷贝仓库到服务器另一个位置 —— 是的，`fork`操作基本上就只是一个服务端的克隆。 `Bitbucket`和`Stash`上可以点一下按钮就让开发者完成仓库的`fork`操作。

这一步完成后，每个开发都在服务端有一个自己的仓库。和正式仓库一样，这些仓库应该是裸仓库。

#### 开发者克隆自己`fork`出来的仓库

![image-20200305143807238](../../image/image-20200305143807238.png)

下一步，各个开发者要克隆自己的公开仓库，用熟悉的`git clone`命令。

在这个示例中，假定用`Bitbucket`托管了仓库。记住，如果这样的话各个开发者需要有各自的`Bitbucket`账号， 使用下面命令克隆服务端自己的仓库：

```
git clone https://user@bitbucket.org/user/repo.git
```

相比前面介绍的工作流只用了一个`origin`远程别名指向中央仓库，`Forking`工作流需要2个远程别名 —— 一个指向正式仓库，另一个指向开发者自己的服务端仓库。别名的名字可以任意命名，常见的约定是使用`origin`作为远程克隆的仓库的别名 （这个别名会在运行`git clone`自动创建），`upstream`（上游）作为正式仓库的别名。

```
git remote add upstream https://bitbucket.org/maintainer/repo
```

需要自己用上面的命令创建`upstream`别名。这样可以简单地保持本地仓库和正式仓库的同步更新。 注意，如果上游仓库需要认证（比如不是开源的），你需要提供用户：

```
git remote add upstream https://user@bitbucket.org/maintainer/repo.git
```

这时在克隆和`pull`正式仓库时，需要提供用户的密码。

#### 开发者开发自己的功能

![image-20200305144431174](../../image/image-20200305144431174.png)

在刚克隆的本地仓库中，开发者可以像其它工作流一样的编辑代码、[提交修改](https://www.atlassian.com/git/tutorial/git-basics#!commit)和[新建分支](https://www.atlassian.com/git/tutorial/git-branches#!branch)：

```
git checkout -b some-feature
# Edit some code
git commit -a -m "Add first draft of some feature"
```

所有的修改都是私有的直到`push`到自己公开仓库中。如果正式项目已经往前走了，可以用[`git pull`命令](https://www.atlassian.com/git/tutorial/remote-repositories#!pull)获得新的提交：

```
git pull upstream master
```

由于开发者应该都在专门的功能分支上工作，`pull`操作结果会都是[快进合并](https://www.atlassian.com/git/tutorial/git-branches#!merge)。**`master`只用来和上游仓库同步代码，在`feature`分支上进行功能增加和冲突修改**

**这里有几个问题：**

- 如果是在单独的分支上开发，为什么还要将master和上游仓库同步，只是单纯为了更新代码？还是说将master分支的更改同步到feature分支上，搜集了一下同步的方法，后续可以试下：

  ```
  $ git checkout develop
  $ git rebase master
  ```

- 如果两个开发者开发的功能有交集，功能完成后发起pull request冲突谁来合并

如果你之前是使用`SVN`，`Forking`工作流可能看起来像是一个激进的范式切换（paradigm shift）。 但不要害怕，这个工作流实际上就是在[功能分支工作流](https://github.com/xirong/my-git/blob/master/workflow-feature-branch.md)之上引入另一个抽象层。 不是直接通过单个中央仓库来分享分支，而是把贡献代码发布到开发者自己的服务端仓库中。

示例中解释了，一个贡献如何从一个开发者流到正式的`master`分支中，但同样的方法可以把贡献集成到任一个仓库中。 比如，如果团队的几个人协作实现一个功能，可以在开发之间用相同的方法分享变更，完全不涉及正式仓库。

这使得`Forking`工作流对于松散组织的团队来说是个非常强大的工具。任一开发者可以方便地和另一开发者分享变更，任何分支都能有效地合并到正式代码库中。

## 五、Pull Request

`Pull requests`是`Bitbucket`提供的让开发者更方便地进行协作的功能，提供了友好的`Web`界面可以在提议的修改合并到正式项目之前对修改进行讨论。

![image-20200305150301855](../../image/image-20200305150301855.png)

​																						bitbucket

![image-20200305150358476](../../image/image-20200305150358476.png)

​																							github

开发者向团队成员通知功能开发已经完成，`Pull Requests`是最简单的用法。 开发者完成功能开发后，通过`Bitbucket`账号发起一个`Pull Request`。 这样让涉及这个功能的所有人知道要去做`Code Review`和合并到`master`分支。

但是，`Pull Request`远不止一个简单的通知，而是为讨论提交的功能的一个专门论坛。 如果变更有任何问题，团队成员反馈在`Pull Request`中，甚至`push`新的提交微调功能。 所有的这些活动都直接跟踪在`Pull Request`中。

![image-20200305150444026](../../image/image-20200305150444026.png)

相比其它的协作模型，这种分享提交的形式有助于打造一个更流畅的工作流。 `SVN`和`Git`都能通过一个简单的脚本收到通知邮件；但是，讨论变更时，开发者通常只能去回复邮件。 这样做会变得杂乱，尤其还要涉及后面的几个提交时。 `Pull Requests`把所有相关功能整合到一个和`Bitbucket`仓库界面集成的用户友好`Web`界面中。

### 5.1 解析`Pull Request`

当要发起一个`Pull Request`，你所要做的就是请求（`Request`）另一个开发者（比如项目的维护者） 来`pull`你仓库中一个分支到他的仓库中。这意味着你要提供4个信息以发起`Pull Request`： 源仓库、源分支、目的仓库、目的分支。

![image-20200305150540193](../../image/image-20200305150540193.png)

这几值多数`Bitbucket`都会设置上合适的缺省值。但取决你用的协作工作流，你的团队可能会要指定不同的值。 上图显示了一个`Pull Request`请求合并一个功能分支到正式的`master`分支上，但可以有多种不同的`Pull Request`用法。

## 5.2  工作方式

`Pull Request`可以和[功能分支工作流](https://github.com/xirong/my-git/blob/master/workflow-feature-branch.md)、[`Gitflow`工作流](https://github.com/xirong/my-git/blob/master/workflow-gitflow.md)或[`Forking`工作流](https://github.com/xirong/my-git/blob/master/workflow-forking.md)一起使用。 但一个`Pull Request`要求要么分支不同要么仓库不同，所以不能用于[集中式工作流](https://github.com/xirong/my-git/blob/master/workflow-centralized.md)。 在不同的工作流中使用`Pull Request`会有一些不同，但基本的过程是这样的：

1. 开发者在本地仓库中新建一个专门的分支开发功能。
2. 开发者`push`分支修改到公开的`Bitbucket`仓库中。
3. 开发者通过`Bitbucket`发起一个`Pull Request`。
4. 团队的其它成员`review` `code`，讨论并修改。
5. 项目维护者合并功能到官方仓库中并关闭`Pull Request`。

本文后面内容说明，`Pull Request`在不同协作工作流中如何应用。
