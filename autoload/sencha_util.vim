" Sencha Utility Vim Plugin
" Last Change: 2014/08/07
" Maintainer: Tanaka Yuuya <yuuya@tnker.com>


let s:save_cpo = &cpo
set cpo&vim

function! sencha_util#Toggle(param)
    let data = s:ParseParam(a:param)
    let name = data.name
    if name =~ "Controller$"
        call s:OpenViewModel(data)
    elseif name =~ "Model$"
        call s:OpenView(data)
    else
        call s:OpenViewController(data)
    endif
endfunction

function! s:OpenView(data)
    let name = a:data.name
    if name =~ "Controller$"
        let name = substitute(name, "Controller$", "", "g")
    elseif name =~ "Model$"
        let name = substitute(name, "Model$", "", "g")
    endif
    let path = "/" . join([join(a:data.paths, "/"), join([name, a:data.ext], ".")], "/")
    let file = getftype(path)
    if file != ""
        exe "e " . path
    endif
endfunction

function! s:OpenViewController(data)
    let name = a:data.name
    if name !~ "Controller$"
        if name =~ "Model$"
            let name = substitute(name, "Model$", "", "g")
        endif
        let name = name . "Controller"
    endif
    let path = "/" . join([join(a:data.paths, "/"), join([name, a:data.ext], ".")], "/")
    let file = getftype(path)
    if file != ""
        exe "e " . path
    endif
endfunction

function! s:OpenViewModel(data)
    let name = a:data.name
    if name !~ "Model$"
        if name =~ "Controller$"
            let name = substitute(name, "Controller$", "", "g")
        endif
        let name = name . "Model"
    endif
    let path = "/" . join([join(a:data.paths, "/"), join([name, a:data.ext], ".")], "/")
    let file = getftype(path)
    if file != ""
        exe "e " . path
    endif
endfunction

function! s:ParseParam(param)
    let paths = split(a:param, "/")
    let filename = remove(paths, -1)
    let name = split(filename, "\\.")[0]
    let ext = split(filename, "\\.")[1]
    return {"paths": paths, "filename": filename, "name": name, "ext": ext}
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
