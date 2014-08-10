" Sencha Utility Vim Plugin
" Last Change: 2014/08/07
" Maintainer: Tanaka Yuuya <yuuya@tnker.com>

if exists("g:loaded_sencha_util")
    finish
endif

let g:loaded_sencha_util = 1

let s:save_cpo = &cpo
set cpo&vim

command! -nargs=0 SenchaMVVMToggle call sencha_mvvm_toggle#Toggle(expand("%:p"))
command! -nargs=0 SenchaMapping call sencha_mapping#Mapping(expand("%:p"))

let &cpo = s:save_cpo
unlet s:save_cpo
