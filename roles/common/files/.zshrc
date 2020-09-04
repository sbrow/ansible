source ~/.zplug/init.zsh

zplug 'zplug/zplug', hook-build:'zplug --self-manage'

zstyle ":zplug:tag" from oh-my-zsh

# Theme
zplug "lib/spectrum"
zplug "lib/prompt_info_functions"
zplug "plugins/git"
zplug "themes/af-magic", as:theme, on:"plugins/git", on:"lib/spectrum", on:"lib/prompt_info_functions"

zplug "plugins/vi-mode"
#zplug "plugins/common-aliases"
zplug "plugins/history"
zplug "plugins/sudo"
zplug "plugins/zsh_reload"
zplug "zsh-users/zsh-syntax-highlighting", from:github, defer:2

# Install plugins if there are plugins that have not been installe
if ! zplug check --verbose; then
    printf "Install? [y/N]: "
    if read -q; then
        echo; zplug install
    fi
fi

# Then, source plugins and add commands to $PATH
zplug load \
# --verbose

# Theme related
typeset +H my_gray="$FG[237]"
typeset +H my_orange="$FG[214]"

setopt auto_cd auto_pushd extended_glob hist_ignore_dups pushd_ignore_dups
