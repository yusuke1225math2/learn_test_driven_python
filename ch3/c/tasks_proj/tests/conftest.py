import pytest
import tasks
from tasks import Task

# @pytest.fixture(scope='session', params=['tiny',])
@pytest.fixture(scope='session', params=['tiny','mongo'])
def tasks_db_session(tmpdir_factory, request):
    # db_typeをパラメトライズ
    # tmpdir_factoryに変更。sessionスコープでdb利用
    """Connect to db before tests, disconnect after."""
    temp_dir = tmpdir_factory.mktemp('temp')
    # セットアップ：dbへの接続を開始
    tasks.start_tasks_db(str(temp_dir), request.param)
    yield # ここでテストを実行
    # ティアダウン：dbへの接続を終了
    tasks.stop_tasks_db()

@pytest.fixture()
def tasks_db(tasks_db_session):
    """空のDB"""
    tasks.delete_all()

### Taskコンストラクタのインタフェースについて
# Task(summary=None, owner=None, done=False, id=None)
# summary:必須, owner/doneはオプション, idはDBにより生成
@pytest.fixture(scope='session')
def tasks_just_a_few():
    return (
        Task('Write some code', 'Brian', True),
        Task("Code review Brian's code", 'Katie', False),
        Task('Fix what Brian did', 'Michelle', False),
    )

@pytest.fixture(scope='session')
def tasks_mult_per_owner():
    return (
        Task('Use an emoji', 'Raphael'),
        Task('Make a cookie', 'Raphael'),
        Task('Move to Berlin', 'Raphael'),
        Task('Create', 'Michelle'),
        Task('Inspire', 'Michelle'),
        Task('Encourage', 'Michelle'),
        Task('Do a handstand', 'Daniel'),
        Task('Write some books', 'Daniel'),
        Task('Eat ice cream', 'Daniel')
    )

@pytest.fixture()
def db_with_3_tasks(tasks_db, tasks_just_a_few):
    for t in tasks_just_a_few:
        tasks.add(t)

@pytest.fixture()
def db_with_multi_per_owner(tasks_db, tasks_mult_per_owner):
    for t in tasks_mult_per_owner:
        tasks.add(t)
