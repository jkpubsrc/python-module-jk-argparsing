The module `jk_argparsing` supports bash completion. (Bash completion is a very convenient feature of the bash shell used on *nix systems.)
The nexts subsections explain how this feature can be used in your own CLI tools.

System bash completion
----------------------------------------------------------------

For bash completion to work you need to run the `complete` commands in the proper way. Typically this is done by having a separate file in a specific system
directory for every command you want to have completion for.
Typically your `~/.basrc` file is constructed in such a way that it reads and sources those files. This way bash completion is enabled in your shell: If you
now enter some letters and press tab your bash shell will try to perform autocompletion.

User bash completion
----------------------------------------------------------------

However, if you want to add non-system bash completion information you have to source proper completion files yourself. That means: a) You need a suitable directory for the
bash completion files in your local home directory and b) you need to source them on login.

This sourcing of user completion files can be done from within the `~/.bashrc` file.

Configuring your account for bash completion with `jk_argsparsing`
----------------------------------------------------------------

For own completion files you can use whatever directory you like. A typical directory would be:

* `~/.bash_completion.d/`

However with a lot of dot-files and -directories your home directory will become a bit confusing. Therefore `jk_argparsing` recommends another directory:

* `~/.config/bash_completion.d/`

In order to enable bash completion make sure that any of these directories exist.

As statet before this sourcing of files from any of these directories can be done from within the `~/.bashrc` file. To enable this you have to modify your `~/.bashrc` file.
Modify the corresponding section in this file to reflect the following fragment:

```bash
# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
  if [ -d ~/.config/bash_completion.d ]; then
    for bcfile in ~/.config/bash_completion.d/* ; do
      [ -f "$bcfile" ] && . $bcfile
    done
  fi
fi
```

As you can see `~/.config/bash_completion.d/` is used here.

Automatically write bash completion files
----------------------------------------------------------------

Now `jk_argsparsing` can be used in such a way that it automatically writes bash completion files to one of these bash completion directories mentioned above.
For this you have to first configure your `ArgsParser` object and then execute the following method:

* `installLocalBashCompletionFile()`

This method will then try to create a file in the bash completion directory for bash completion.

NOTE: A file will only be written if it does not exist or if the bash completion data has changed. So typically for users this file is only written once.

Please note that bash completion will only work after sourcing the file written. As this is done on login (if `.bashrc` is designed properly) the completion will
take affect on next login (or if you manually source the completion file).

The method `installLocalBashCompletionFile()` is designed to operate silently. However you can modify it's behavior by providing some options:

| Argument												| Description		|
| ---													| ---				|
| `bool bQuiet = False`									| If you set this argument to `True` some status output for errors or actions taken.			|
| `function printFunc = None`							| If you want to use a different function for writing output instead of `print` specifiy your own function here.	|
| `str[] dirCandidates = None				`			| By default `installLocalBashCompletionFile()` will use the directories listed in `BASH_COMPLETION_DIR_CANDIDATES`. However if you wish to specify a completely different set, provide it here.	|
| `bool bRaiseExceptionIfNoCompletionDirExists = False`	| If you want an exception to be raised if the current user account is not configured for supporting bash completion, you can set this argument to `True`.	|










