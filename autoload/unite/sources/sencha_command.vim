" Sencha Utility Vim Plugin
" Last Change: 2014/08/07
" Maintainer: Tanaka Yuuya <yuuya@tnker.com>

let s:save_cpo = &cpo
set cpo&vim

" ----------
" setting source
let s:unite_sencha_command = {
\    "name"         : "sencha"
\   ,"description"  : "Sencha Command Utility"
\   ,"action_table" : {
\       "build_production": {
\           "description": "Sencha Application Production Build"
\       }
\      ,"build_testing": {
\           "description": "Sencha Application Testing Build"
\       }
\      ,"build_package": {
\           "description": "Sencha Application Package Build"
\       }
\   }
\   ,"default_action": "production_build"
\}

" ----------
" functions
function! s:unite_sencha_command.action_table.build_production.func(candidate)
    echo "PRODUCTION BUILD"
endfunction

function! s:unite_sencha_command.action_table.build_testing.func(candidate)
    echo "TESTING BUILD"
endfunction

function! s:unite_sencha_command.action_table.build_package.func(candidate)
    echo "PACKAGE BUILD"
endfunction

" ----------
" return unite param
function! s:unite_sencha_command.gather_candidates(args, context)
    return [
    \   {"word": "TEST1", "source": "senchacmd"}
    \  ,{"word": "TEST2", "source": "senchacmd"}
    \]
endfunction

" ----------
" register source
function! unite#sources#sencha_command#define()
    return s:unite_sencha_command
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo

