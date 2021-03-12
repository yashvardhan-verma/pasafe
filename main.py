import sqlite3 as sq3
from generator import generate_pass
from colored import fg, bg, attr

connection = sq3.connect('passwords.db')
cursor = connection.cursor()

def commit_and_close():
    connection.commit()
    connection.close()

def interface():
    print("%s%sWelcome To Pass-lock.%s" %(fg('orchid'), attr('bold'), attr('reset')))
    print("%s[0].%s %s Get your Password %s" %(fg(1), attr('bold'), fg(86), attr('bold')))
    print("%s[1].%s %s Add a New Password. %s" %(fg(1), attr('bold'), fg(86), attr('bold')))
    print("%s[2].%s %s Update a Existing Password. %s" %(fg(1), attr('bold'), fg(86), attr('bold')))
    print("%s[3].%s %s See all Passwords. %s" %(fg(1), attr('bold'), fg(86), attr('bold')))
    print("")
    pass_choice = int(input("%s %sEnter Your Choice. %s" %(bg('indian_red_1a'), fg('white'), attr('reset'))))
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
    cursor.execute("SELECT * FROM passwords WHERE web_name = '%s'" %website_name)
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
        website_password = input("Enter Password for %s : " %website_name)

    sql = "Insert into passwords values ('%s', '%s', '%s')" %(website_name, u_name, website_password)
    cursor.execute(sql)
    print("password Added.")

def update_pass():
    website_name = input("Enter Website/App name : ")
    new_password = input("Enter New Password : ")
    cursor.execute("update passwords set password = '%s' where web_name = '%s'" %(new_password, website_name))
    commit_and_close()

def see_all():
    cursor.execute('select * from passwords')
    data = cursor.fetchall()
    for row in data:
        for col in row:
            print(col, end=" ")
        print()

if __name__ == '__main__':
    interface()
