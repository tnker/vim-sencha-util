" Sencha Utility Vim Plugin
" Last Change: 2014/08/07
" Maintainer: Tanaka Yuuya <yuuya@tnker.com>

let s:save_cpo = &cpo
set cpo&vim

" source定義
let s:unite_sencha_command = {
\    'name' : 'sencha'
\ }

function! s:unite_sencha_command.gather_candidates(args, context)
    return [
    \    {"word": "TEST1", "source": "senchacmd", "kind": "word"}
    \  , {"word": "TEST2", "source": "senchacmd", "kind": "word"}
    \ ]
endfunction

" source登録
function! unite#sources#sencha_command#define()
    return s:unite_sencha_command
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo

