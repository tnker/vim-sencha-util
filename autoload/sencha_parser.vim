" Sencha Parser Vim Plugin
" Last Change: 2015/08/06
" Maintainer: Tanaka Yuuya <yuuya@tnker.com>
"
let s:save_cpo = &cpo
set cpo&vim

pyfile <sfile>:h:h/src/sencha.py
python import vim
python sencha = SenchaParser()

function! sencha_parser#openviewmodel(file)
    python sencha.setup(vim.eval('a:file'))
    python viewmodel = sencha.get_viewmodel(vim.eval('a:file'))
    python sencha.open_file(vim, viewmodel)
endfunction

function! sencha_parser#openviewcontroller(file)
    python sencha.setup(vim.eval('a:file'))
    python viewcontroller = sencha.get_controller(vim.eval('a:file'))
    python sencha.open_file(vim, viewcontroller)
endfunction

function! sencha_parser#readcurrentline(file)
    python sencha.setup(vim.eval('a:file'))
    python sencha.load_file(vim.eval('a:file'))
    python classname, cnt = sencha.read_line(vim.current.line)
    python sencha.open_file(vim, classname, cnt)
endfunction

function! sencha_parser#getrequires(file)
    python sencha.setup(vim.eval('a:file'))
    python result = sencha.get_requires(vim.eval('a:file'))
    return pyeval('result')
endfunction

function! sencha_parser#getextendtree(file)
    python sencha.setup(vim.eval('a:file'))
    python result = sencha.get_extend_tree(vim.eval('a:file'))
    return pyeval('result')
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
