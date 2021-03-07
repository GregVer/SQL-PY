import psycopg2
import pandas as pd
import sqlalchemy
from pw import *
import sys
import time
import platform
import subprocess


def clear():
    subprocess.Popen("cls" if platform.system() == "Windows" else "clear", shell=True)
    time.sleep(0.1)


def question(task_number):
    print("Continue to the " + task_number + " task? y/n")
    answer = input()
    if answer == "y":
        return "yes"
    elif answer == "n":
        return "no"
    else:
        question(task_number)


def print_todo_table(task_number, engine, query_todo=None):
    clear()
    print("Result of " + task_number + " task:\n")
    print("Todo table:\n")
    if query_todo is not None:
        todo_table = pd.read_sql(query_todo, engine)
    else:
        todo_table = pd.read_sql_table('todo', engine)
    print(todo_table)
    print("------------------------------------\n")


def print_user_table(engine, query_user=None):
    print("")
    print("------------------------------------\n")
    print("User table:\n")
    if query_user is not None:
        user_table = pd.read_sql(query_user, engine)
    else:
        user_table = pd.read_sql_table('user', engine)
    print(user_table)
    print("------------------------------------\n")


user_name = "postgres"
host = "localhost"
database_name = "tododb"

connect_str = "postgresql://{user_name}:{password}@{host}/{database_name}".format(
    user_name=user_name,
    password=password,
    host=host,
    database_name=database_name
)

connection = psycopg2.connect(connect_str)
connection.autocommit = True
cursor = connection.cursor()

engine = sqlalchemy.create_engine("postgresql://postgres:" + password + "@localhost:5432/tododb")

cursor.execute("DROP TABLE IF EXISTS todo; DROP TABLE IF EXISTS \"user\";")

cursor.execute('''
CREATE TABLE \"user\" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE todo (
    id SERIAL PRIMARY KEY,
    task VARCHAR(100),
    user_id int,
    FOREIGN KEY (user_id) REFERENCES \"user\"(id)
);
''')

query_todo = '''select column_name, data_type, character_maximum_length, column_default, is_nullable
from INFORMATION_SCHEMA.COLUMNS where table_name = 'todo';'''
print_todo_table("first", engine, query_todo)

query_user = '''select column_name, data_type, character_maximum_length, column_default, is_nullable
from INFORMATION_SCHEMA.COLUMNS where table_name = 'user';'''
print_user_table(engine, query_user)

anwser_returned = question("second")
if anwser_returned == "yes":
    cursor.execute('''
    ALTER TABLE todo
    ADD done BOOLEAN DEFAULT 'false';
    ''')

    query_todo = '''select column_name, data_type, character_maximum_length, column_default, is_nullable
    from INFORMATION_SCHEMA.COLUMNS where table_name = 'todo';'''
    print_todo_table("second", engine, query_todo)

    anwser_returned = question("third")
    if anwser_returned == "yes":

        cursor.execute('''
        INSERT INTO \"user\" (name)
        VALUES ('Jane');
        INSERT INTO \"user\" (name)
        VALUES ('John');
        INSERT INTO \"user\" (name)
        VALUES ('Dave');
        INSERT INTO \"user\" (name)
        VALUES ('Emma');
        INSERT INTO \"user\" (name)
        VALUES ('Robert');
        INSERT INTO todo (task, user_id)
        VALUES ('Setup pgAdmin', '2');
        INSERT INTO todo (task, user_id)
        VALUES ('Download Git', '2');
        INSERT INTO todo (task, user_id, done)
        VALUES ('Setup VS Code', '1', 'true');
        INSERT INTO todo (task, user_id)
        VALUES ('Download  PostgreSQL', '2');
        INSERT INTO todo (task, user_id)
        VALUES ('Install server', '2');
        INSERT INTO todo (task, user_id)
        VALUES ('Create superuser', '2');
        INSERT INTO todo (task, user_id)
        VALUES ('Create database', '2');
        INSERT INTO todo (task, user_id)
        VALUES ('Create tables', '2');
        INSERT INTO todo (task, user_id)
        VALUES ('Wash the dishes', '3');
        INSERT INTO todo (task, user_id)
        VALUES ('Read the PostgreSQL manual', '4');
        INSERT INTO todo (task, user_id)
        VALUES ('Exercise', '3');
        INSERT INTO todo (task, user_id, done)
        VALUES ('Wake up in time!', '5', 'true');
        INSERT INTO todo (task, user_id)
        VALUES ('Go to the gym', '3');
        INSERT INTO todo (task, user_id, done)
        VALUES ('Wash the dishes', '5', 'true');
        ''')

        user_table = pd.read_sql_table('user', engine)
        todo_table = pd.read_sql_table('todo', engine)
        print_todo_table("third", engine)
        print_user_table(engine)

        anwser_returned = question("fourth")
        if anwser_returned == "yes":
            query_todo = '''
            SELECT * FROM todo WHERE done = 'true';
            '''
            print_todo_table("fourth", engine, query_todo)

            anwser_returned = question("fifth")
            if anwser_returned == "yes":
                query_todo = '''
                UPDATE todo
                SET done = 'true'
                WHERE user_id = '2';

                SELECT * FROM todo
                ORDER BY id;
                '''
                print_todo_table("fifth", engine, query_todo)

                anwser_returned = question("sixth")
                if anwser_returned == "yes":
                    cursor.execute('''
                    DELETE FROM todo WHERE done = 'true';
                    ''')

                    print_todo_table("sixth", engine)

                    anwser_returned = question("seventh")
                    if anwser_returned == "yes":
                        cursor.execute('''
                        DROP TABLE todo;
                        DROP TABLE \"user\";
                        ''')
                        clear()
                        print("Result of seventh task:\n")
                        try:
                            todo_table = pd.read_sql_table('todo', engine)
                            print(todo_table)
                        except ValueError:
                            print("Todo table has been dropped!\n")
                        try:
                            user_table = pd.read_sql_table('user', engine)
                            print(user_table)
                        except ValueError:
                            print("User table has been dropped!\n")
                            time.sleep(10)

                    else:
                        sys.exit()
                else:
                    sys.exit()
            else:
                sys.exit()
        else:
            sys.exit()
    else:
        sys.exit()
else:
    sys.exit()
