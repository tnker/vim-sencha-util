#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import json
import re

# {{{ class SenchaParser_Info

class SenchaParser_Info(object):

    workspace_path = None

    app_path = None

    major_version = None

    full_version = None

    framework_name = None

    current_path = None

    is_classic = False

    is_modern = False

    re = None

    # {{{ __init__()

    def __init__(self, re):
        self.re = re

    # }}}
    # {{{ setup(path)

    def setup(self, path):
        """
        ルートディレクトリパス取得
        """
        self.app_path = self.__get_sencha_dir(path)
        self.workspace_path = self.__get_workspace_dir(path)
        """
        フレームワーク情報取得
        """
        config_path = '{0}/.sencha/app/sencha.cfg'.format(self.app_path)
        if os.path.isfile(config_path):
            fp = open(config_path)
            ln = fp.readline()
            is_framework_version = False
            is_framework_name = False
            while ln:
                if not is_framework_version:
                    is_framework_version = self.__parse_framework_version(ln)
                if not is_framework_name:
                    is_framework_name = self.__parse_framework_name(ln)
                if is_framework_version and is_framework_name:
                    break
                ln = fp.readline()
            fp.close()
        """
        ExtJS6の場合はext固定
        """
        if self.is_version('6'):
            self.framework_name = 'ext'

    # }}}
    # {{{ load(path)

    def load(self, path):
        self.__set_src_dir(path)
        self.current_path = path

    # }}}
    # {{{ is_version(major_version, minor_version = None)

    def is_version(self, major_version, minor_version = None):
        return major_version == self.major_version

    # }}}
    # {{{ __set_src_dir(path)

    def __set_src_dir(self, path):
        """
        プロジェクトディレクトリ以外のフォルダ名が
        該当した場合、フラグが立ってしまうので要修正
        """
        if self.is_version('6'):
            self.is_classic = 'classic' in path
            self.is_modern = 'modern' in path

    # }}}
    # {{{ __get_sencha_dir(path)

    def __get_sencha_dir(self, path):
        parent_path = os.path.abspath(os.path.dirname(path))
        path = None
        paths = parent_path.split('/')
        while len(paths) > 1:
            tmp_path = '/'.join(paths)
            is_sencha_dir = os.path.isdir('{0}/.sencha'.format(tmp_path))
            if is_sencha_dir:
                path = tmp_path
                break
            else:
                paths = paths[:-1]
        return path

    # }}}
    # {{{ __get_workspace_dir(path)

    def __get_workspace_dir(self, path):
        parent_path = os.path.abspath(os.path.dirname(path))
        path = None
        paths = parent_path.split('/')
        while len(paths) > 1:
            tmp_path = '/'.join(paths)
            is_sencha_dir = os.path.isdir('{0}/.sencha/workspace'.format(tmp_path))
            if is_sencha_dir:
                path = tmp_path
                break
            else:
                paths = paths[:-1]
        return path

    # }}}
    # {{{ __parse_framework_version(string)

    def __parse_framework_version(self, string):
        m = self.re.framework_version.search(string)
        if m:
            self.full_version = m.groups()[0]
            self.major_version = self.full_version[:1]
            return True
        return False

    # }}}
    # {{{ __parse_framework_name(string)

    def __parse_framework_name(self, string):
        m = self.re.framework_name.search(string)
        if m:
            self.framework_name = m.groups()[0]
            return True
        return False

    # }}}

# }}}
# {{{ class SenchaParser_Regex

class SenchaParser_Regex(object):
    """SenchaPaeserパッケージ上で利用する正規表現を一元管理用

    Attributes:
        appname: アプリケーションの名前空間マッチ用
        framework_version: sencha.cfgからsdkバージョン抽出用
        xtype_name: xtypeで指定されている文字列を取得する
        framework_name: sencha.cfgから利用SDKタイプ抽出用
        extend_comment: Doc形式のコメントから継承元クラス抽出用（overrideと併用）
        extend_property: コンフィグ内から継承元クラス抽出用（overrideと併用）
        class_comment: Doc形式のコメントからクラス名抽出用
        class_define: コード内のdefineメソッド引数からクラス名抽出用
        namespace: コード内のシングル／ダブルクオォートで括られた文字列抽出用
        requires_st: requires句の開始位置判断用
        requires_ed: requires句の終了位置判断用
        alias: 文字列で定義されているalias句抽出用
        alias_st: alias句の開始位置判断用
        alias_ed: alias句の終了位置判断用
        alias_type: alias句内のaliasに該当する文字列抽出用
        handler: xxx
    """
    appname = re.compile('^([\w]+)\.')
    framework_version = re.compile('^[\s]*app.framework.version[\s]*=[\s]*([0-9¥.]+)$')
    framework_name = re.compile('^[\s]*app.framework[\s]*=[\s]*([a-zA-Z]+)$')
    xtype_name = re.compile('^[\s]*xtype[\s]*:[\s]*\'([a-zA-Z\-\_]+)\'[\s\,]*$')
    extend_comment = re.compile('^.+@(extend|override)[ ]+(.+)')
    extend_property = re.compile('^.+(extend|override)[ :]+[ ]+\'(.+)\'')
    class_comment = re.compile('^.+@class[ ]+(.+)')
    class_define = re.compile('^Ext.define\([\W\']+([\w\.]+)[\W\']')
    namespace = re.compile('[\s]*[\'\"]([\S]+)[\'\"]')
    requires_st = re.compile('^[\s]*requires*[\s]*:[\s]*\[*[\s]*(([\'\"a-zA-Z\.,\s])*)[\s]*\]*')
    requires_ed = re.compile('[\s]*\]')
    alias = re.compile('[\s]*(controller|viewModel)[\s]*:[\s]*[\'\"]([\S]+)[\'\"]')
    alias_st = re.compile('[\s]*(controller|viewModel)[\s]*:[\s]*\{[\s]*$')
    alias_ed = re.compile('[\s]*\}[\s,]*$')
    alias_type = re.compile('^[\s]*type[\s]*:[\s]*[\'\"]([\S]+)[\'\"]')
    handler = re.compile('^[\s]*[\sa-zA-Z]*:[\s]*[\"\']([a-zA-Z]*)[\"\'][\s,]*')

# }}}
# {{{ class SenchaParser_Common

class SenchaParser_Common(object):

    # {{{ __init__()

    def __init__(self):
        self.re = SenchaParser_Regex()
        self.info = SenchaParser_Info(self.re)

    # }}}

# }}}
# {{{ class SenchaParser_Base

class SenchaParser_Base(object):

    __instance = None

    # {{{ __init__()

    def __init__(self):
        if SenchaParser_Base.__instance is None:
            SenchaParser_Base.__instance = SenchaParser_Common()
        super(SenchaParser_Base, self).__init__()

    # }}}
    # {{{ getter.re

    @property
    def re(self):
        return SenchaParser_Base.__instance.re

    # }}}
    # {{{ getter.info

    @property
    def info(self):
        return SenchaParser_Base.__instance.info

    # }}}

# }}}
# {{{ class SenchaParser

class SenchaParser(SenchaParser_Base):

    __class_name = None

    __extend_name = None

    __override_name = None

    __controller_alias = None

    __is_controller_alias_loading = False

    __viewmodel_alias = None

    __is_viewmodel_alias_loading = False

    __requires = None

    __bootstrap = None

    # {{{ __init__()

    def __init__(self):
        self.__bootstrap = SenchaParser_Bootstrap()
        self.__requires = SenchaParser_Requires()
        super(SenchaParser, self).__init__()

    # }}}
    # {{{ setup(path)

    def setup(self, path):
        """
        設定情報ロード
        """
        self.info.setup(path)
        """
        バージョンに応じたapp/bootstrap.jsonを辞書型で取得
        """
        self.__bootstrap.load(
            self.info.app_path
        )

    # }}}
    # {{{ load_file(path)

    def load_file(self, path, is_update = True):
        """
        参照コードが設置ディレクトリチェック
        """
        if is_update:
            self.info.load(path)
        """
        """
        if os.path.isfile(path):
            fp = open(path)
            ln = fp.readline()
            while ln:
                self.__parse_class_name(ln)
                self.__parse_extend_name(ln)
                self.__parse_controller_alias(ln)
                self.__parse_viewmodel_alias(ln)
                self.__requires.read_line(ln)
                ln = fp.readline()
            fp.close()

    # }}}
    # {{{ open_file(vim, path, row_index = 0)

    def open_file(self, vim, path, row_index = 0):
        print(path)
        if vim and path and self.info.current_path != path:
            if os.path.isfile(path):
                vim.command('tabnew {0}'.format(path))
                vim.command('{0}'.format(row_index))
        elif vim and path and self.info.current_path == path:
            vim.command('{0}'.format(row_index))

    # }}}
    # {{{ read_line(line)

    def read_line(self, line):
        cnt = 0
        """
        xtypeに指定されている文字列から取得
        """
        path = self.get_xtype(line)
        """
        """
        if not path:
            path, cnt = self.get_handler(self.info.current_path, line)
        """
        シングルクォーテーションで括られている
        文字列からクラス名の取得を試みる
        """
        if not path:
            m = self.re.namespace.search(line)
            if m:
                path = self.get_class(class_name=m.groups()[0])
        return (path, cnt)

    # }}}
    # {{{ get_class(line, class_name, is_path = True)

    def get_class(self, line = None, class_name = None, is_path = True):
        if not class_name and line:
            m = self.re.namespace.search(line)
            if m:
                class_name = m.groups()[0]
        if is_path:
            return self.__convert_class_to_path(class_name)
        else:
            return class_name

    # }}}
    # {{{ get_xtype(line, is_path = True)

    def get_xtype(self, line, is_path = True):
        m = self.re.xtype_name.search(line)
        if m:
            class_name = self.__bootstrap.search(m.groups()[0], 'widget')
            return self.get_class(class_name=class_name)
        return None

    # }}}
    # {{{ get_controller(path, is_path = True)

    def get_controller(self, path, is_path = True):
        self.load_file(path)
        class_name = self.__bootstrap.search(
            self.__controller_alias,
            'controller'
        )
        if is_path:
            return self.__convert_class_to_path(class_name)
        else:
            return class_name

    # }}}
    # {{{ get_viewmodel(path, is_path = True)

    def get_viewmodel(self, path, is_path = True):
        self.load_file(path)
        class_name = self.__bootstrap.search(
            self.__viewmodel_alias,
            'viewmodel'
        )
        if is_path:
            return self.__convert_class_to_path(class_name)
        else:
            return class_name

    # }}}
    # {{{ get_handler(path, line)

    def get_handler(self, path, line):
        m = self.re.handler.search(line)
        if m:
            func_name = m.groups()[0]
            func_path = path
            func_path, cnt = self.__parse_function_name(func_path, func_name)
            if func_path:
                return (func_path, cnt)
        else:
            return (None, 0)
        require_paths = self.get_requires(path)
        for class_path in require_paths:
            ctrl_path = self.get_controller(class_path)
            func_path, cnt = self.__parse_function_name(ctrl_path, func_name)
            if func_path:
                return (func_path, cnt)
        return (None, 0)

    # }}}
    # {{{ get_requires(path)

    def get_requires(self, path):
        self.__dispose()
        self.load_file(path, False)
        class_name = self.__class_name
        app_name = self.__parse_app_name(class_name)
        dir_name = self.__convert_base_to_path(app_name)
        requires = self.__requires.search_required(
            self.info,
            dir_name,
            class_name)
        if not requires:
            dir_name = self.__convert_base_to_path(None)
            requires = self.__requires.search_required(
                self.info,
                dir_name,
                class_name)
        return requires

    # }}}
    # {{{ __parse_app_name(string)

    def __parse_app_name(self, string):
        m = self.re.appname.search(string)
        if not m:
            return ''
        return m.groups()[0]

    # }}}
    # {{{ __parse_function_name(path, func_name)

    def __parse_function_name(self, path, func_name):
        m = None
        p = '{0}[\s]*:[\s]*[\s]*function[\s]*\(([A-Z,a-z0-9\s]*)\)'.format(func_name)
        try:
            if os.path.isfile(path):
                fp = open(path)
                ln = fp.readline()
                cnt = 1
                while ln:
                    m = re.search(p, ln)
                    if m:
                        break
                    ln = fp.readline()
                    cnt += 1
                fp.close()
            if m:
                return (path, cnt)
            else:
                return (None, 0)
        except:
            return (None, 0)

    # }}}
    # {{{ __parse_class_name(string)

    def __parse_class_name(self, string):
        if string is None or self.__class_name:
            return True
        m = self.re.class_comment.search(string)
        if m:
            self.__class_name = m.groups()[0]
            return True
        m = self.re.class_define.search(string)
        if m:
            self.__class_name = m.groups()[0]
            return True
        return False

    # }}}
    # {{{ __parse_extend_name(string)

    def __parse_extend_name(self, string):
        if string is None or self.__extend_name or self.__override_name:
            return True
        m = self.re.extend_comment.search(string)
        if m:
            if m.groups()[0] == 'extend':
                self.__extend_name = m.groups()[1]
            else:
                self.__override_name = m.groups()[1]
            return True
        m = self.re.extend_property.search(string)
        if m:
            if m.groups()[0] == 'extend':
                self.__extend_name = m.groups()[1]
            else:
                self.__override_name = m.groups()[1]
            return True
        return False

    # }}}
    # {{{ __parse_controller_alias(string)

    def __parse_controller_alias(self, string):
        if string is None or self.__controller_alias:
            return True
        if not self.__is_controller_alias_loading:
            m = self.re.alias.search(string)
            if m and m.groups()[0] == 'controller':
                self.__controller_alias = m.groups()[1]
                return True
            m = self.re.alias_st.search(string)
            if m:
                self.__is_controller_alias_loading = True
                m = self.re.alias_type.search(string)
                if m:
                    self.__controller_alias = m.groups()[0]
                    self.__is_controller_alias_loading = False
                    return True
        else:
            m = self.re.alias_type.search(string)
            if m:
                self.__controller_alias = m.groups()[0]
                self.__is_controller_alias_loading = False
                return True

        return False

    # }}}
    # {{{ __parse_viewmodel_alias(string)

    def __parse_viewmodel_alias(self, string):
        if string is None or self.__viewmodel_alias:
            return True
        if not self.__is_viewmodel_alias_loading:
            m = self.re.alias.search(string)
            if m and m.groups()[0] == 'viewModel':
                self.__viewmodel_alias = m.groups()[1]
                return True
            m = self.re.alias_st.search(string)
            if m:
                self.__is_viewmodel_alias_loading = True
                m = self.re.alias_type.search(string)
                if m:
                    self.__viewmodel_alias = m.groups()[0]
                    self.__is_viewmodel_alias_loading = False
                    return True
        else:
            m = self.re.alias_type.search(string)
            if m:
                self.__viewmodel_alias = m.groups()[0]
                self.__is_viewmodel_alias_loading = False
                return True

    # }}}
    # {{{ __convert_class_to_path(class_name)

    def __convert_class_to_path(self, class_name):
        if not class_name:
            return ''
        info = self.info
        dir_name = ''
        src_path = ''
        """
        """
        app_name = self.__parse_app_name(class_name)
        """
        クラス名とファイルパスをコンバートする前に
        現状開いているSenchaアプリのバージョン情報
        を判断してパス生成処理を変える
        """
        dir_name = self.__convert_base_to_path(app_name)
        """
        コンバート対象クラスがSenchaの基底クラスの場合は
        参照先ディレクトリ名を上書き
        FIXME: sencha-core等のパッケージを参照している場合の対応
        """
        if app_name and app_name.lower() == 'ext':
            app_path = info.workspace_path
            """
            通常のSDK配下にある前提でパスを生成する
            TODO: 外部メソッドもしくはクラスに分離したほうが良い？
            """
            class_path = self.re.appname.sub(dir_name, class_name)
            class_path = class_path.replace('.', '/') + '.js'
            src_path = '{0}/{1}'.format(app_path, class_path)
            if not os.path.isfile(src_path):
                if self.info.is_version('6'):
                    dir_name = 'packages/core/src/'
                else:
                    dir_name = 'packages/sencha-core/src/'
                if app_path.split('/')[-1:][0] != info.framework_name:
                    dir_name = '{0}/{1}'.format(
                        info.framework_name,
                        dir_name)
                class_path = self.re.appname.sub(dir_name, class_name)
                class_path = class_path.replace('.', '/') + '.js'
                src_path = '{0}/{1}'.format(app_path, class_path)
        else:
            app_path = info.app_path
            class_path = self.re.appname.sub(dir_name, class_name)
            class_path = class_path.replace('.', '/') + '.js'
            src_path = '{0}/{1}'.format(app_path, class_path)
            if not os.path.isfile(src_path):
                dir_name = 'app/'
                app_path = info.app_path
                class_path = self.re.appname.sub(dir_name, class_name)
                class_path = class_path.replace('.', '/') + '.js'
                src_path = '{0}/{1}'.format(app_path, class_path)
        return src_path

    # }}}
    # {{{ __convert_base_to_path(app_name)

    def __convert_base_to_path(self, app_name):
        info = self.info
        dir_name = ''
        if app_name and app_name.lower() == 'ext':
            if self.info.is_version('6'):
                if info.is_classic:
                    dir_name = '{0}/classic/classic/src/'.format(info.framework_name)
                elif info.is_modern:
                    dir_name = '{0}/modern/modern/src/'.format(info.framework_name)
            else:
                dir_name = '{0}/src/'.format(info.framework_name)
        else:
            if self.info.is_version('6'):
                if info.is_classic:
                    dir_name = 'classic/src/'
                elif info.is_modern:
                    dir_name = 'modern/src/'
                else:
                    dir_name = 'app/'
            else:
                dir_name = 'app/'
        return dir_name

    # }}}
    # {{{ __dispose()

    def __dispose(self):
        self.__class_name = None
        self.__override_name = None
        self.__viewmodel_alias = None
        self.__controller_alias = None
        self.__is_viewmodel_alias_loading = False
        self.__is_controller_alias_loading = False

    # }}}

# }}}
# {{{ class SenchaParser_Bootstrap

class SenchaParser_Bootstrap(SenchaParser_Base):

    __app = None

    __bootstrap = None

    __modern = None

    __classic = None

    # {{{ getter.app

    @property
    def app(self):
        return self.__app

    # }}}
    # {{{ getter.bootstrap

    @property
    def bootstrap(self):
        return self.__bootstrap

    # }}}
    # {{{ getter.modern

    @property
    def modern(self):
        return self.__modern

    # }}}
    # {{{ getter.classic

    @property
    def classic(self):
        return self.__classic

    # }}}
    # {{{ load(app_dir)

    def load(self, app_dir):
        if self.info.is_version('6'):
            self.__modern = self.__load_json(app_dir, 'modern')
            self.__classic = self.__load_json(app_dir, 'classic')
        else:
            self.__bootstrap = self.__load_json(app_dir, 'bootstrap')

        self.__app = self.__load_json(app_dir)

    # }}}
    # {{{ search(alias, prefix)

    def search(self, alias, prefix):
        temp = None
        if not alias:
            return temp
        try:
            if self.info.is_version('6'):
                if not temp:
                    temp = self.__search_alias(alias, prefix, self.classic['classes'])
                if not temp:
                    temp = self.__search_alias(alias, prefix, self.modern['classes'])
            else:
                temp = self.__search_alias(alias, prefix, self.bootstrap['classes'])
        except:
            return ''
        return temp

    # }}}
    # {{{ __load_json(sencha_dir_path, name = 'app')

    def __load_json(self, app_dir, name = 'app'):
        json_path = '{0}/{1}.json'.format(app_dir, name)
        if os.path.isfile(json_path):
            try:
                fp = open(json_path)
                json_data = fp.read()
                fp.close()
                return json.loads(json_data)
            except:
                return None
        else:
            return None

    # }}}
    # {{{ __search_alias(alias, prefix, info)

    def __search_alias(self, alias, prefix, info):
        for k, v in info.items():
            if v:
                if '{0}.{1}'.format(prefix, alias) in v['alias']:
                    return k

    # }}}

# }}}
# {{{ class SenchaParser_Requires

class SenchaParser_Requires(SenchaParser_Base):

    __is_loading = False

    __classes = []

    # {{{ getter.classes

    @property
    def classes(self):
        return self.__classes

    # }}}
    # {{{ load_file(path)

    def load_file(self, path, class_name):
        """
        指定したスクリプトに指定したクラスがrequire
        されているかをチェックし、されている場合は
        スクリプトのファイルパスを返却する
        """
        m = None
        p = '[\s]*requires[\s]*:[\s]*\[[\s\S]*{0}'.format(class_name)
        try:
            if os.path.isfile(path):
                fp = open(path)
                ln = fp.read()
                m = re.search(p, ln)
                fp.close()
            if m:
                return path
            else:
                return None
        except:
            return None

    # }}}
    # {{{ read_line(line)

    def read_line(self, line):
        temp = None
        if not self.__is_loading:
            m = self.re.requires_st.search(line)
            if m:
                self.__is_loading = True
                temp = self.re.namespace.findall(line)
        else:
            temp = self.re.namespace.findall(line)
            m = self.re.requires_ed.search(line)
            if m:
                self.__is_loading = False
        if temp:
            self.__classes = self.__classes + temp

    # }}}
    # {{{ search_required(info, dir_name, class_name)

    def search_required(self, info, dir_name, class_name):
        requires = []
        dir_path = '{0}/{1}'.format(info.app_path, dir_name)
        for file_path in self.__find_all_files(dir_path):
            required = self.load_file(file_path, class_name)
            if required:
                requires.append(file_path)
        return requires

    # }}}
    # {{{ __find_all_files(dir_path)

    def __find_all_files(self, dir_path):
        for root, dirs, files in os.walk(dir_path):
            yield root
            for file in files:
                yield os.path.join(root, file)

    # }}}

# }}}
# {{{ class SenchaParser_Package

class SenchaParser_Package(SenchaParser_Base):

    # {{{ load(name)

    def load(self, name):
        pass

    # }}}

# }}}


def sencha_util_test(vim, path):
    _sup = SenchaParser()
    _sup.setup(path)
    _sup.get_handler(path, '   handler: "onNewRecordForm"')
    #print(_sup.get_controller(path))
    #print(_sup.get_viewmodel(path))
    #path = _sup.get_class("   extend: 'App.view.base.Menu',")
    #if vim:
    #    vim.command('tabnew {0}'.format(path))
    #else:
    #    print(path)

#sencha_util_test(None, '/Users/tnker/Sites/ws_touch241c/cordova/app/view/Menu.js')
#sencha_util_test(None, '/Users/tnker/Sites/ws_ext600b/money/app/modern/src/view/revenue/List.js')

