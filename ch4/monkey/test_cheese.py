import copy
import cheese

def test_def_prefs_full():
    cheese.write_default_cheese_preferences()
    expected = cheese._default_prefs
    actual = cheese.read_cheese_preferences()
    assert expected == actual

def test_def_prefs_change_home(tmpdir, monkeypatch):
    monkeypatch.setenv('HOME', tmpdir.mkdir('home'))
    cheese.write_default_cheese_preferences()
    expected = cheese._default_prefs
    actual = cheese.read_cheese_preferences()
    assert expected == actual

def test_def_prefs_change_expanduser(tmpdir, monkeypatch):
    fake_home_dir = tmpdir.mkdir('home')
    monkeypatch.setattr(
        cheese.os.path, 'expanduser',
        lambda x: x.replace('~', str(fake_home_dir))
    )
    cheese.write_default_cheese_preferences()
    expected = cheese._default_prefs
    actual = cheese.read_cheese_preferences()
    assert expected == actual

def test_def_prefs_change_defaults(tmpdir, monkeypatch):
    # ファイルを一度だけ書き出す
    fake_home_dir = tmpdir.mkdir('home')
    monkeypatch.setattr(
        cheese.os.path, 'expanduser',
        lambda x: x.replace('~', str(fake_home_dir))
    )
    cheese.write_default_cheese_preferences()
    defaults_before = copy.deepcopy(cheese._default_prefs)

    # デフォルト値を変更する
    monkeypatch.setitem(cheese._default_prefs, 'slicing', ['provolone'])
    monkeypatch.setitem(cheese._default_prefs, 'spreadable', ['brie'])
    monkeypatch.setitem(cheese._default_prefs, 'salads', ['pepper jack'])
    defaults_modified = cheese._default_prefs

    # 変更されたデフォルトでもう一度書き出す
    cheese.write_default_cheese_preferences()

    # ファイルを読み込んでチェックする
    actual = cheese.read_cheese_preferences()
    assert defaults_modified == actual
    assert defaults_modified != defaults_before
