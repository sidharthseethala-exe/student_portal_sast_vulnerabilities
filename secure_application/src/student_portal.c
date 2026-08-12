#include <stdio.h>
#include <sqlite3.h>

int loggedIn = 0;
int myId = 101; // to store curr 

void setup(sqlite3 *db)
{
    char *err = 0;

    sqlite3_exec(db,
        "CREATE TABLE IF NOT EXISTS students("
        "id INTEGER, username TEXT, password TEXT,"
        "name TEXT, grade TEXT, email TEXT);",
        0, 0, &err);

    sqlite3_exec(db, // to delte all exisiting rec o stat new
        "DELETE FROM students;",
        0, 0, &err);

    sqlite3_exec(db,
        "INSERT INTO students VALUES"
        "(101,'alice','1234','Alice','A','alice@gmail.com');",
        0, 0, &err);

    sqlite3_exec(db,
        "INSERT INTO students VALUES"
        "(102,'bob','5678','Bob','B','bob@gmail.com');",
        0, 0, &err);
}

void login(sqlite3 *db)
{
    char user[50], pass[50], sql[200];
    sqlite3_stmt *stmt;// stores the prepared sql statement 

    printf("\nUsername: ");
    scanf("%s", user);

    printf("Password: ");
    scanf("%s", pass);

    /* vulnerability 1: sql injection */
    // can return student even though we did not provide a real username ex :'OR'1'='1 by attacker thts true and thats sql commmnd 
    // it basicaly takes whatever the user types and puts directky in thte sql command 
    sprintf(sql,
        "SELECT id FROM students WHERE username='%s' AND password='%s'",
        user, pass);

    sqlite3_prepare_v2(db, sql, -1, &stmt, 0);

    if (sqlite3_step(stmt) == SQLITE_ROW)
    {
        loggedIn = 1;
        myId = sqlite3_column_int(stmt, 0);
        printf("Login successful!\n");
    }
    else
    {
        printf("Login failed!\n");
    }

    sqlite3_finalize(stmt);
}

void grades(sqlite3 *db)
{
    int id;
    char sql[100];
    sqlite3_stmt *stmt;

    printf("\nEnter student ID: ");
    scanf("%d", &id); // you directly ask and use no authroizaton

    /* Vulnerability 2: IDOR */ 
    // insecure direct object refrence -- 101 can acess 102 grade
    sprintf(sql, "SELECT name,grade FROM students WHERE id=%d", id);

    sqlite3_prepare_v2(db, sql, -1, &stmt, 0);

    if (sqlite3_step(stmt) == SQLITE_ROW)
    {
        printf("Name: %s\n", sqlite3_column_text(stmt, 0));
        printf("Grade: %s\n", sqlite3_column_text(stmt, 1));
    }

    sqlite3_finalize(stmt);
}

void update(sqlite3 *db)
{
    int id;
    char email[50];
    char sql[150];

    printf("\nEnter student ID: ");
    scanf("%d", &id);

    printf("New email: ");
    scanf("%s", email);

    /* Vulnerability 3: Missing Authorization */
    // it knows who you are but does not check you are allowed or not 
    sprintf(sql,
        "UPDATE students SET email='%s' WHERE id=%d",
        email, id);

    sqlite3_exec(db, sql, 0, 0, 0);

    printf("Profile updated!\n");
}

void course()
{
    char name[50];

    printf("\nEnter course name: ");
    scanf("%s", name);

    printf("Course %s registered!\n", name);
}

int main()
{
    sqlite3 *db;
    int choice;

    sqlite3_open("students.db", &db);

    setup(db);

    printf("student portal ---\n");

    login(db);

    if (!loggedIn)
    {
        sqlite3_close(db);
        return 0;
    }

    while (1)
    {
        printf("\n1. Register Course\n");
        printf("2. View Grades\n");
        printf("3. Update Profile\n");
        printf("4. Exit\n");

        printf("Choice: ");
        scanf("%d", &choice);

        if (choice == 1)
            course();

        else if (choice == 2)
            grades(db);

        else if (choice == 3)
            update(db);

        else if (choice == 4)
            break;

        else
            printf("Wrong choice!\n");
    }

    sqlite3_close(db);

    return 0;
}
