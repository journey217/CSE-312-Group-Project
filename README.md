# CSE-312-Group-Project



Website Link:
[jessebay.us](jessebay.us)





## Make Sure Pull Before Push

~~~
git add *
~~~
* This means add <b>all</b> files.

~~~
git commit -m "a short descripton"
~~~

* Then, commit to your local repository.

* You should check if any changes have been created to the remote repository before psuh.
~~~
git pull
~~~
* <b>If you ignore this process, the source code in the repository will be tangled.</b>
<br>

~~~
git push origin branch
~~~
* Now push the changes

## Branch
~~~
git branch <branch_name>
~~~
* Create "<branch_name>"</b>
~~~
git branch -b <branch_name>
~~~
* Move to the "<branch_name>"</b>
~~~
git branch -d <branch_name>
~~~
* Delete the "<branch_name>"
## Alias
~~~
[alias]
    lg = lg1
    lg1 = lg1-specific --all
    lg2 = lg2-specific --all
    lg3 = lg3-specific --all

    lg1-specific = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(auto)%d%C(reset)'
    lg2-specific = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(auto)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)'
    lg3-specific = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset) %C(bold cyan)(committed: %cD)%C(reset) %C(auto)%d%C(reset)%n''          %C(white)%s%C(reset)%n''          %C(dim white)- %an <%ae> %C(reset) %C(dim white)(committer: %cn <%ce>)%C(reset)'
~~~
Add 3 aliases (and 4 alias-aliases for quick usage) in my ~/.gitconfig file. It helps to follow commit logs

