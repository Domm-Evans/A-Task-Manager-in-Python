#username: dominic
#password: evans

#register user r
#add a task a
#view all tasks va
#view current user's task vm
    #display all tasks neatly and numbered
    #select by number or -1 to return to menu
    #once selected can mark task as complete or edit if complete change y/n label
    #when editting can edit user name assigned to or due date
#generate reports gr
    #generate txt file task_overview and user_overview should be generated and output data
    #task overview contains, total task, no completed tasks, no. uncompleted, no. overdue_incomplete, % incomplete, %overdue_incomplete
    #user overview contains, total no. users, total no. tasks, no. tasks assigned to user, % etc etc
#display statistics ds
#exit e

#functions r, a va, vm

from datetime import datetime, date

#read user function opens username txt file reads all usernames and passwords and adds to list
def read_users():
    file = open("user.txt","r")
    for lines in file:
        temp = lines.strip()
        temp = temp.split(";")
        usernames.append(temp[0])
        passwords.append(temp[1])
    file.close()

#read tasks from txt file and append to relevant lists
def initialise_tasks():
    file = open("tasks.txt", "r")
    for i, lines in enumerate(file):
        temp = lines.strip()
        temp = temp.split(";")
        task_ids.append(i+1)
        task_username.append(temp[0])
        task_title.append(temp[1])
        task_desc.append(temp[2])
        task_due.append(temp[3])
        completed.append(temp[4])
    file.close()

#reads tasks from txt file and updates the lists (rather than appends) with any changes
def read_tasks():
    file = open("tasks.txt", "r")
    for i, lines in enumerate(file):
        temp = lines.strip()
        temp = temp.split(";")
        task_ids[i] = i + 1
        task_username[i] = temp[0]
        task_title[i] = temp[1]
        task_desc[i] = temp[2]
        task_due[i] = temp[3]
        completed[i] = temp[4]
    i = 0
    file.close()

#login function
def login():
    read_users()
    global logged_in            #checks log in status
    logged_in = False
    while not logged_in:        #loop for users not logged in requests login details and cross references them to database
        print("Welcome to login:")
        global username, password
        username = input("Username: ")
        password = input("Password: ")
        if username not in usernames:
            print("Sorry username is incorrect \n")
        elif password not in passwords:
            print("Sorry password is incorrect \n")
        elif usernames.index(username) == passwords.index(password):    #checks username and passwords are paired
            print(f"""Congratulations you've logged in
    Welcome {username} please access the menu here: """)
            logged_in = True
            menu()
        else:
            print("Sorry try again")

#function to write to file to save on space in other areas
def write_to_file(file_name,line_in,task_index):
    out_file = open(file_name, "r+")
    lines = out_file.readlines()
    lines[task_index] = line_in
    out_file.seek(0)
    out_file.writelines(lines)
    out_file.close()

#menu options 
def menu():
    global logged_in
    while logged_in:
        #print menu list offering options for the user to select
        print("""\nMake a selection from below:   
        Register user (r)
        Add a new task (a)
        View all tasks (va)
        View Current Task (vm)
        Generate reports (gr)
        Display statistics (ds)
        Exit (e)\n""")
        
        #direct to correct function based on user selection
        selection = input("Input the code in the brackets for the selection you want: ").lower()
        if selection == "r":
            reg_user()
        elif selection == "a":
            add_task()
        elif selection == "va":
            view_all_task()
        elif selection == "vm":
            view_mine()
        elif selection == "gr":
            gen_reports()
        elif selection == "ds":
            statistics()
        elif selection == "e":
            logged_in = False
        else:
            print("Invalid selection")
    login()

#register user function that takes new password and username and confirms password, adds to user.txt database
def reg_user():
    print("\nYou've selected you want to register a user input login details below:\n")  
    new_username = input("Username: ")
    new_password = input("Password: ")
    confirm_password = input("Confirm Password: ")
    if new_username in usernames:                       #checks if username is available
        print("\nSorry that username is unavaiable \n")
        reg_user()
    elif new_password != confirm_password:              #checks new password matches confirmation
        print("\nPasswords do not match try again\n")
        reg_user()
    else:
        out_file = open("user.txt", "a")
        out_file.write(f"\n{new_username};{new_password}")
        print("\nThis user is now registered, log in to view tasks\n")
        out_file.close()
        logged_in = False
        login()

#add new task function that takes user input for each task area and adds to tasks.txt file
def add_task():
    print("\nYou've selected add task, complete the details below: ")
    assigned_user = input("Assigned User: ")
    new_task_title = input("Task Title: ")
    new_task_desc = input("Task Description: ")
    due_date_string = input("Task Due Date Year: YYYY-MM-DD: ")
    new_task_due_date = datetime.strptime(due_date_string, "%Y-%m-%d").date()
    task_completed = "no"
    if assigned_user not in usernames:              #check username exists in the database
        print("\nSorry that user does not exist\n")
    elif new_task_due_date < current_date:          #checks date is in future
        print("\nThis date is in the past\n")
    else:
        out_file = open("tasks.txt", "a")
        out_file.write(f"\n{assigned_user};{new_task_title};{new_task_desc};{due_date_string};{task_completed}")
        out_file.close()
        task_ids.append(len(task_ids)+1)
        task_username.append(assigned_user)
        task_title.append(new_task_title)
        task_desc.append(new_task_desc)
        task_due.append(due_date_string)
        completed.append(task_completed)
        print("This task has been successfully added\n")
        menu()
    add_task()

#view all tasks functions, reads the tasks to update component lists and prints each component to terminal in user-friendly manner
def view_all_task():
    read_tasks()
    for i in range(0,len(task_username)):
        print(f"-----------------------------[{task_ids[i]}]--------------------------------------")
        print(f"Assigned to:\t\t{task_username[i]}")
        print(f"Task Title:\t\t{task_title[i]} ")
        print(f"Task Description:\t{task_desc[i]} ")
        print(f"Due Date:\t\t{task_due[i]}")
        print(f"Completed: \t\t{completed[i]}")
    menu()

#views the users tasks
def view_mine():
    read_tasks()                                        #re_reads tasks to include updates
    #loops through for the length of each task list and indexes the information where the username matches the logged in user
    for i in range(0,len(task_username)):
        if username == task_username[i]:                
            print(f"-----------------------------[{task_ids[i]}]--------------------------------------")
            print(f"Assigned to:\t\t{task_username[i]}")
            print(f"Task Title:\t\t{task_title[i]} ")
            print(f"Task Description:\t{task_desc[i]} ")
            print(f"Due Date:\t\t{task_due[i]}")
            print(f"Completed: \t\t{completed[i]}")
            username_indexes.append(i)                                              #makes list of the task indexes assigned to the user
    #obtains user input to select task from options and prints
    task_selection = int(input("""\nSelect which task you would like to mark as complete or edit using the task id
or input '-1' to return to menu: """))
    task_index = task_selection-1
    if task_selection == int(-1):                                                   #takes you back to menu with "-1" input
        menu()
    elif task_selection not in task_ids or task_index not in username_indexes :     #removes incorrect inputs and prevents editting of others' tasks
        print("\nIncorrect task id, please choose a correct task id")
        menu()
    else: 
        print("\nYou've selected: ")
        print(f"-----------------------------[{task_ids[task_index]}]--------------------------------------")
        print(f"Assigned to:\t\t{task_username[task_index]}")
        print(f"Task Title:\t\t{task_title[task_index]} ")
        print(f"Task Description:\t{task_desc[task_index]} ")
        print(f"Due Date:\t\t{task_due[task_index]}")
        print(f"Completed: \t\t{completed[task_index]}")
    edit_complete = input("Would you like to edit (e) or complete (c) the task? Input c or e ").lower()
    
#allows the user to choose if they want to edit the username or date, or mark as completed
    if edit_complete == "e" and completed[task_index] == "no":          #allows it to be editted if it hasn't already been completed
        print("\nYou've selected edit task, complete the details below: ")
        assigned_user = input("Assigned User: ")
        due_date_string = input("Task Due Date Year: YYYY-MM-DD: ")
        new_task_due_date = datetime.strptime(due_date_string, "%Y-%m-%d").date()
        task_username[task_index] = assigned_user
        task_due[task_index] = new_task_due_date
        if new_task_due_date < date.today():                            #if due date is set to past takes back to menu
            print("\nThis due date is in the past")
            menu()
        elif assigned_user not in usernames:                            #checks username is in the database
            print("\nUnknown user")
            menu()
        else:                                                           #writes to file at the same line
            tasks_line_in = f"{assigned_user};{task_title[task_index]};{task_desc[task_index]};{new_task_due_date};{completed[task_index]}\n"
            task_file_name = "tasks.txt"
            write_to_file(task_file_name, tasks_line_in, task_index)
            print("This task has been successfully edited\n")
            menu()
    
    #if "mark as complete" is selected rewrites the line in the file to change the "completed" component
    elif edit_complete == "c":
        completed[task_index] = "yes"
        task_file_name = "tasks.txt"
        tasks_line_in = f"{task_username[task_index]};{task_title[task_index]};{task_desc[task_index]};{task_due[task_index]};{completed[task_index]}\n"
        write_to_file(task_file_name, tasks_line_in, task_index)
        print("\nThis task has been marked has completed, this cannot be undone")
        menu()
    elif edit_complete == "e" and completed[task_index] != "no":        #prevents user from editting completed tasks
        print("\nYou cannot edit completed tasks")
        menu()
    else:
        print("\nIncorrect response")
        menu()
    read_tasks()

#function to generate reports and open and write to task_overview.txt and user_overview.txt files
def gen_reports():
    task_report, user_report = open("task_overview.txt","w"), open("user_overview.txt", "w")
    #appends indexes of tasks where date has surpassed to list of 'indexes overdue'
    overdue_index_list = []                                                             #indexes of overdue tasks in list
    for i, val in enumerate(task_due):
        due_date = datetime.strptime(val, "%Y-%m-%d").date()
        if due_date < date.today():
            overdue_index_list.append(i)

    incomplete_index_list = [i for i, val in enumerate(completed) if val == "no"]       #indexes of non completed tasks in list
    
    #number of tasks both overdue_incomplete and incomplete
    overdue_incomplete = 0
    for i in overdue_index_list:
        if i in incomplete_index_list:              #checks which indexes occur in both overdue and incomplete lists and counts
            overdue_incomplete += 1

    total_tasks = len(task_ids)                                         #total number of tasks
    total_tasks_completed = completed.count("yes")                      #no.tasks completed
    total_tasks_incompleted = len(task_ids) - total_tasks_completed     #no. tasks incomplete
    per_incomplete = round((total_tasks_incompleted/total_tasks)*100,2)     #percentage tasks incomplete
    per_overdue = round((overdue_incomplete/total_tasks)*100,2)               #percentage tasks overdue

    #writes stats to txt file in a user-friendly manner
    task_report.write(f"""The task completetion statistics:\n
    {total_tasks} - The total number of tasks generated.
    {total_tasks_completed} - The total number of compeleted tasks.
    {total_tasks_incompleted} - The total number of incompelete tasks.
    {overdue_incomplete} - The total number of tasks overdue.

    %{per_incomplete} - The percentage of tasks that are incomplete.
    %{per_overdue} - The percentage of tasks that are overdue.\n""")

    total_num_users = len(usernames)                            #total number of users
    users_total_tasks = task_username.count(username)           #number of tasks assigned to user
    user_perc_of_total_tasks = round((users_total_tasks/total_tasks)*100,2)     #users percentage of total tasks

    #if task indexes assigned to the user are incomplete add to counter
    users_tasks_index = [i for i, val in enumerate(task_username) if val == username]   #builds list of indexes of tasks with users username
    users_tasks_incomplete = 0
    for i in users_tasks_index:
        if i in incomplete_index_list:                      #if users task index matches with incomplet task index add one to counter
            users_tasks_incomplete += 1
    perc_users_tasks_complete = round(((users_total_tasks - users_tasks_incomplete)/users_total_tasks)*100,2)   #percentage of users tasks completed
    perc_users_tasks_incomplete = round((users_tasks_incomplete/users_total_tasks)*100,2)                       #percentage of users tasks incomplete

    #repeats process to calculate number overdue and incomplete
    users_overdue_incomplete = 0
    for i in overdue_index_list:
        if i in incomplete_index_list and i in users_tasks_index:       ###if overdue index matches with users task index and incomplete 
            users_overdue_incomplete += 1                               ###index list then add to counter
    perc_users_overdue_tasks = round((users_overdue_incomplete/users_total_tasks)*100,2)    #percentage of users tasks overdue and incomplete

    #writes the stats to user_report.txt in a user friendly manner
    user_report.write(f"""{username.capitalize()}'s task completion statistics:\n
    {total_num_users} - The total number of users.
    {total_tasks} - The total number of tasks generated.
    {users_total_tasks} - Your total number of tasks assigned.

    %{user_perc_of_total_tasks} - The percentage of all tasks assigned to you.
    %{perc_users_tasks_complete} - The percentage of your tasks you've completed.
    %{perc_users_tasks_incomplete} - The percentage of your tasks that are incomplete.
    %{perc_users_overdue_tasks} - The percentage of your tasks overdue.\n""")
    user_report.close()
    task_report.close()

#function to print statistics to terminal
def statistics():
    gen_reports()       #calls generate report function to make calculations
    user_report, task_report = open("user_overview.txt","r", encoding = "utf-8"), open("task_overview.txt","r", encoding = "utf-8")
    u_report, t_report = user_report.read(), task_report.read() 
    print(t_report)
    print(u_report)

#main
logged_in = False
usernames,passwords,task_username, task_title, task_desc,task_due,completed,task_ids,username_indexes = [],[],[],[],[],[],[],[],[]
current_date = date.today()

read_users()
initialise_tasks()
login()



    