" Sencha Utility Vim Plugin
" Last Change: 2014/08/07
" Maintainer: Tanaka Yuuya <yuuya@tnker.com>

if exists("g:loaded_sencha_mvvm_toggle")
    finish
endif

let g:loaded_sencha_mvvm_toggle = 1

let s:save_cpo = &cpo
set cpo&vim

if !hasmapto("<Plug>SenchaToggle")
    map <unique> <C-@> <Plug>SenchaToggle
endif

noremap <unique> <script> <Plug>SenchaToggle <SID>Toggle
noremap <SID>Toggle :call <SID>Toggle(expand("%:p"))<CR>

let &cpo = s:save_cpo
unlet s:save_cpo
