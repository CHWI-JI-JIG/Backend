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
        choices=["test", "django", "migrate", "delete-storage"],  # "git-push",
        default="django",
    )
    # parser.add_argument("--branch", default="main")
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", default=5000)
    parser.add_argument("--db_attach", type=str, default="log_")
    parser.add_argument("--storage_type", default="mysql")
    parser.add_argument(
        "--ver",
        choices=["python"],
        default="python",
    )
    parser.add_argument(
        "--test_file",
        nargs="*",
        default=[
            r"Tests\Members\test_builder.py",
            r"Tests\Members\test_member_service.py",
            r"Tests\Members\test_user_migrate.py",
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
    from Migrations import MySqlCreateProduct, MySqlCreateUser

    m_p = MySqlCreateProduct(get_db_padding())
    m_m = MySqlCreateUser(get_db_padding())
    if m_p.check_exist_product():
        m_p.delete_product()
    if m_m.check_exist_user():
        m_m.delete_user()


def migrate():
    from Migrations import MySqlCreateProduct, MySqlCreateUser

    m_p = MySqlCreateProduct(get_db_padding())
    m_m = MySqlCreateUser(get_db_padding())

    delete_storage()
    m_m.create_user()
    # m_p.create_product()


# def set_storage(storage_type: str):
#     from Infrastructures.IOC import select_strage

#     select_strage(storage_type)


def main(opt):
    from icecream import ic
    from get_config_data import set_db_padding

    global db_name
    debug = opt.debug

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
        case "django":
            print("Not Impliment Djanpo.")
        case "migrate":
            migrate()
        case "delete-storage":
            delete_storage()
        case _:
            print("'python manage.py -h' 명령어도 인자를 확인해 주세요.")


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
