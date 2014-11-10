" Sencha Utility Vim Plugin
" Last Change: 2014/08/07
" Maintainer: Tanaka Yuuya <yuuya@tnker.com>

let s:save_cpo = &cpo
set cpo&vim

"let s:V    = vital#of('vital')
"let s:JSON = s:V.import('Web.JSON')

" ----------
" sencha functions
function! sencha_mapping#Mapping(param)
    let data = s:ParseParam(a:param)
    let path = []
    while len(data.paths) > 0
        let p = "/" . join(data.paths, "/")
        let s = getftype(p . "/streamline.json")
        let m = getftype(p . "/microfield.json")
        if s != ""
            call s:StreamlineMapping(p)
            break
        endif
        if m != ""
            call s:MicroFieldMapping(p)
            break
        endif
        let f = getftype(p . "/.sencha")
        if f != ""
            let info = system("cat " . p . "/app.json")
            " TODO: 正規表現でJSONのコメントの掃除したいけど
            " ちょっとうまくいかないので一旦あきらめる
            "let json = s:JSON.decode(info)
            let pkgs = s:GetClassName(getline("."))
            let oPath = s:GetFilePath(pkgs)
            if oPath != ""
                call s:OpenClassFile(join([p, oPath], "/"))
            endif
            break
        endif
        unlet data.paths[-1]
    endwhile
    if len(data.paths) == 0
        echo "not found .sencha"
    endif
endfunction

function! s:GetClassName(line)
    let store = matchstr(a:line, "store[\ ]*:.*$")
    let name = matchstr(a:line, "[\"\'].*[\"\']", 0)
    let name = substitute(name, "[\"\']", "", "g")
    let pkgs = split(name, "\\.")
    if store != ""
        return ["app", "store"] + pkgs
    else
        return pkgs
    endif
endfunction

function! s:GetFilePath(pkgs)
    if len(a:pkgs) != 0
        let pkgs = a:pkgs
        let app = remove(pkgs, 0)
        if app == "Ext"
            call insert(pkgs, "ext/src", 0)
        else
            call insert(pkgs, "app", 0)
        endif
        return join(pkgs, "/") . ".js"
    else
        return ""
    endif
endfunction

" ----------
" streamline functions
function! s:StreamlineMapping(rPath)
    let pkgs = s:GetClassName(getline("."))

    if pkgs[0] == "Streamline"
        call insert(pkgs, "app", 1)
    else
        call insert(pkgs, "app", 2)
    endif

    let path = join(pkgs, "/") . ".js"
    if matchstr(path, ":") != ""
        let lang = split(path, ":")
        call remove(lang, 1)
        call add(lang, "locales/lang-ja.json")
        let path = join(lang, "/")
        call s:OpenClassFile(join([a:rPath, path], "/"))
    else
        call s:OpenClassFile(join([a:rPath, path], "/"))
    endif
endfunction

" ----------
" microfield functions
function! s:MicroFieldMapping(rPath)
    let pkgs = s:GetClassName(getline("."))

    if pkgs[0] == "MicroField"
        call insert(pkgs, "app", 1)
    else
        call insert(pkgs, "app", 2)
    endif

    let path = join(pkgs, "/") . ".js"
    if matchstr(path, ":") != ""
        let lang = split(path, ":")
        call remove(lang, 1)
        call add(lang, "locales/lang-ja.json")
        let path = join(lang, "/")
        call s:OpenClassFile(join([a:rPath, path], "/"))
    else
        call s:OpenClassFile(join([a:rPath, path], "/"))
    endif
endfunction

" ----------
" utility functions
function! s:OpenClassFile(path)
    let file = getftype(a:path)
    if file != ""
        exe "tabnew " . a:path
    else
        echo "not found class file: " . a:path
    endif
endfunction

function! s:ParseParam(param)
    try
        let paths = split(a:param, "/")
        let filename = remove(paths, -1)
        let name = split(filename, "\\.")[0]
        let ext = split(filename, "\\.")[1]
        let param = {"paths": paths, "filename": filename, "name": name, "ext": ext}
    catch
        let param = {"paths": []}
    endtry
    return param
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo

