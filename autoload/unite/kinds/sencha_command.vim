" Sencha Utility Vim Plugin
" Last Change: 2014/08/07
" Maintainer: Tanaka Yuuya <yuuya@tnker.com>

let s:save_cpo = &cpo
set cpo&vim

let s:kind = {}
let s:kind.name = "sencha"
let s:kind.action_table = {}

let s:kind.action_table.test = {
\   "description" : "test"
\}
function! s:kind.action_table.test.func(candidate)
    execute "echo '" . a:candidate.word . "'"
endfunction

" ----------
" register source
function! unite#kinds#sencha_command#define()
    return s:kind
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo

