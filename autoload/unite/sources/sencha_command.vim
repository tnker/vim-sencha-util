" Sencha Utility Vim Plugin
" Last Change: 2014/08/07
" Maintainer: Tanaka Yuuya <yuuya@tnker.com>

let s:save_cpo = &cpo
set cpo&vim

let s:unite_sources = { 'name' : 'sencha', 'hooks' : {} }

function! s:make_command(command)
    let cmd = a:command
    let cursor_linenr = get(a:000, 0, line('.'))
    let vimfiler = vimfiler#get_current_vimfiler()
    let sep = has('win32') ? ' &' : ';'
    " 別プロセスで実行するかどうか(windowsはどちらにしても別プロセスだから無視)
    let is_bgrun = stridx(cmd, '&') != -1 && !has('win32')
    " ワイルドカード展開の邪魔にならないよう一時的に削除しておく
    let cmd = substitute(cmd, '&', '', 'g')

    " マークされているファイルリストを取得
    " マークがない場合はカーソルのあたっているファイルを選択
    let marked_files = vimfiler#get_marked_files()
    if empty(marked_files)
        let marked_files = [ vimfiler#get_file(cursor_linenr) ]
    endif

    if stridx(cmd, '%*') != -1 || stridx(cmd, '%#') != -1
        let command_list = [ s:expand_filelist(cmd, marked_files) ]
    else
        let command_list = map(marked_files, '
\           s:replace_subwildcard(cmd, v:val.action__path)
\       ')
    endif

    let cmd = (is_bgrun ? 'silent ' : '')
    let cmd = cmd . '!' . join(command_list, sep . ' ')
    let cmd = cmd . (is_bgrun ? '&' : '')
    return cmd
endfunction

function! s:unite_sources.gather_candidates(args, context)
    let sendto = copy(g:vimfiler_sendto)

    return map(keys(sendto), '{
\       "word" : v:val
\     , "source" : "sendto"
\     , "kind" : "command"
\     , "action__command" : s:make_command(sendto[v:val])
\   }')
endfunction

function! unite#sources#sencha_command#define()
    return s:unite_sources
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo

