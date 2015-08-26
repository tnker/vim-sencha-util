" Sencha Utility Vim Plugin
" Last Change: 2014/08/07
" Maintainer: Tanaka Yuuya <yuuya@tnker.com>

let s:save_cpo = &cpo
set cpo&vim

let s:source = {}
let s:source.name = "sencha"

" ----------
" return unite param
function! s:source.gather_candidates(args, context)

    let trees = sencha_parser#getextendtree(expand('%:p'))

    return map(copy(trees), '{
    \   "word": v:val.name,
    \   "kind": "file",
    \   "addr": v:val.path,
    \   "action__path": v:val.path,
    \}')

"    return [
"\       {"word": "TEST1", "addr": "TEST1", "kind": "sencha"}
"\      ,{"word": "TEST2", "addr": "TEST2"}
"\   ]
endfunction

" ----------
" register source
function! unite#sources#sencha_command#define()
    return s:source
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo

