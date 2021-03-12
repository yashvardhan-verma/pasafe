import sqlite3 as sq3
from generator import generate_pass
from colored import fg, bg, attr
import argparse
from os import system, name

connection = sq3.connect('passwords.db')
cursor = connection.cursor()


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def commit_and_close():
    connection.commit()
    connection.close()


def interface():
    clear()
    print("%s%sWelcome To Pass-lock.%s" % (fg('orchid'), attr('bold'), attr('reset')))
    print("%s[0].%s %s Get your Password %s" % (fg(1), attr('bold'), fg(86), attr('bold')))
    print("%s[1].%s %s Add a New Password. %s" % (fg(1), attr('bold'), fg(86), attr('bold')))
    print("%s[2].%s %s Update a Existing Password. %s" % (fg(1), attr('bold'), fg(86), attr('bold')))
    print("%s[3].%s %s See all Passwords. %s" % (fg(1), attr('bold'), fg(86), attr('bold')))
    print("")
    pass_choice = int(input("%sEnter Your Choice. %s" % (fg('white'), attr('reset'))))
    if pass_choice == 0:
        get_pass()
    if pass_choice == 1:
        add_pass()
    if pass_choice == 2:
        update_pass()
    if pass_choice == 3:
        see_all()
    if pass_choice not in [0, 1, 2, 3]:
        print("Wrong Choice.")
        interface()


def get_pass():
    website_name = input(" Enter Website's Name : ")
    cursor.execute("SELECT * FROM passwords WHERE web_name = '%s'" % website_name)
    data = cursor.fetchall()
    if data is not None:
        print(data)
    else:
        print("No data found.")
    commit_and_close()


def add_pass():
    website_name = input("Enter Website's Name : ")
    u_name = input("Enter username : ")
    website_password = input("If you want me to generate a password for you"
                             "then press [Y] for YES and [N] for NO.")
    if website_password == 'Y' or website_password == 'y':
        website_password = generate_pass()
    if website_password == 'N' or website_password == 'n':
        website_password = input("Enter Password for %s : " % website_name)

    sql = "Insert into passwords values ('%s', '%s', '%s')" % (website_name, u_name, website_password)
    cursor.execute(sql)
    print("password Added.")


def update_pass():
    website_name = input("Enter Website/App name : ")
    u_name = input("Enter Username : ")
    new_password = input("Enter New Password : ")
    cursor.execute("update passwords set password = '%s' where web_name = '%s' and username = '%s'" % (
        new_password, website_name, u_name))
    commit_and_close()


def see_all(sitename=None):
    if sitename is None:
        cursor.execute('select * from passwords')
        data = cursor.fetchall()
        for row in data:
            for col in row:
                print(col, end=" ")
            print()
    else:
        cursor.execute("select * from passwords where web_name = '%s'" % sitename)
        data = cursor.fetchall()
        for row in data:
            for col in row:
                print(col, end=" ")
            print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sitename", help="ouputs every password of specified site.", nargs="?", const="interface")
    args = parser.parse_args()
    if args.sitename is None:
        interface()
    else:
        see_all(args.sitename)
