import __init__

import argparse
import os
import subprocess
from icecream import ic

from get_config_data import get_db_padding


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run",
        choices=["test", "flask", "migrate", "delete-storage"],  # "git-push",
        default="flask",
    )
    # parser.add_argument("--branch", default="main")
    parser.add_argument("--not_debug", action="store_true")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", default=5000)
    parser.add_argument("--db_attach", type=str, default="log_")
    parser.add_argument("--storage_type", default="mysql")
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--clear_db_init", action="store_true")
    parser.add_argument(
        "--ver",
        choices=["python", "python3"],
        default="python",
    )
    parser.add_argument(
        "--test_file",
        nargs="*",
        default=[
            r"Tests/Members/test_builder.py",
            r"Tests/Members/test_member_service.py",
            r"Tests/Members/test_user_migrate.py",
            # r"",
        ],
    )
    opt = parser.parse_args()
    return opt


def test(test_list: list, py_v="python") -> bool:
    fail = False

    test_exe = f"{py_v} -m unittest"
    fail_list = []

    for test in test_list:
        test_py = f"{test_exe} {test}"
        print(test_exe, test)
        ret = subprocess.call(test_py, shell=True)
        if ret == 1:
            fail_list.append(test)
            fail = True
    if fail:
        print("=======================Fail Test=============================")
        for test in fail_list:
            print(f"\t> {test}")
        print("=======================+++++++++=============================")

    return not fail


def git_push(test_list: list, branch="main"):
    if test(test_list):
        exe = f"git push origin {branch}"
        subprocess.call(exe, shell=True)


def delete_storage():
    from Migrations import (
        MySqlCreateProduct,
        MySqlCreateUser,
        MySqlCreateComments,
        MySqlCreateSession,
        MySqlCreateOrder,
    )

    p = MySqlCreateProduct(get_db_padding())
    m = MySqlCreateUser(get_db_padding())
    c = MySqlCreateComments(get_db_padding())
    s = MySqlCreateSession(get_db_padding())
    o = MySqlCreateOrder(get_db_padding())
    if s.check_exist_session():
        s.delete_session()
    if c.check_exist_comments():
        c.delete_comments()
    if o.check_exist_order():
        o.delete_order()
    if p.check_exist_product():
        p.delete_product()
    if m.check_exist_user():
        m.delete_user()


def migrate(clear_db_init=False):
    from Migrations import (
        MySqlCreateProduct,
        MySqlCreateUser,
        MySqlCreateComments,
        MySqlCreateSession,
        MySqlCreateOrder,
    )

    p = MySqlCreateProduct(get_db_padding())
    m = MySqlCreateUser(get_db_padding())
    c = MySqlCreateComments(get_db_padding())
    s = MySqlCreateSession(get_db_padding())
    o = MySqlCreateOrder(get_db_padding())

    if clear_db_init:
        delete_storage()

    m.create_user()
    assert m.check_exist_user(), "Dont't exsist User Table."
    p.create_product()
    assert p.check_exist_product(), "Dont't exsist Product Table."
    c.create_comments()
    assert c.check_exist_comments(), "Dont't exsist Comments Table."
    o.create_order()
    assert o.check_exist_order(), "Dont't exsist Orders Table."
    s.create_session()
    assert s.check_exist_session(), "Dont't exsist Session Table."


# def set_storage(storage_type: str):
#     from Infrastructures.IOC import select_strage


#     select_strage(storage_type)
def flask(debug=True, host="127.0.0.1", port=5000):
    from Flask.main import app

    app.run(debug=debug, host=host, port=int(port))


def main(opt):
    from icecream import ic
    from get_config_data import set_db_padding

    global db_name
    debug = not opt.not_debug

    if debug:
        ic.enable()
    else:
        ic.disable()
        set_db_padding(opt.db_attach)

    print(f"Run {opt.run}")
    # set_storage(opt.storage_type)
    match opt.run:
        case "test":
            ic.enable()
            test(opt.test_file, opt.ver)
        # case "git-push":
        #     git_push(opt.test_file, opt.branch)
        case "migrate":
            assert isinstance(
                opt.clear_db_init, bool
            ), "Type of --clear_db_init is bool."
            migrate(opt.clear_db_init)
            assert isinstance(opt.init, bool), "Type of --init is bool."
            from init_data import init_member, init_product,init_comment

            if opt.init:
                init_member()
                init_product()
                init_comment()
        case "flask":
            flask(debug, opt.host, opt.port)
        case "delete-storage":
            delete_storage()
        case _:
            print("'python manage.py -h' 명령어도 인자를 확인해 주세요.")


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
