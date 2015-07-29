# Postgres/PostGIS configurations

In this document we:

1. [Create a new user for Postgresql database](#1)
2. [Open the server (database) to 'listen' the world (i.e. enable other servers/computers to insert data to our database)](#2).
3. [Next steps](#3)

## <a name="1"><a/>1. Create a new user for Postgresql

Before using Postgres/PostGIS it is recommended to set a password to PostgreSQL superuser (postgres) and to create a new user for PostgreSQL database 
that is always used during the data collection (for security reasons).     

Log in as PostgreSQL superuser (postgres)

>   sudo su - postgres

Open PostgreSQL sql-prompt
>   psql

Set password for postgres user in PostgreSQL (keep the password in mind, you will need it!)
>   ALTER ROLE postgres WITH PASSWORD 'my_password';

Exit the sql-prompt by typing
>   \q 

Create a new user (use the same username as when logging in to the Ubuntu)
>   createuser -U postgres -d -E -i -l -P -r -s myUserName
>   >$Password: myPassword

Check that you can log in as psql -U <yourusername>
>   psql -U myUserName template1

## <a name="2"><a/>2. Open the database to listen the world
Before it is possible to use the database remotely we need to make changes to two PostgreSQL configuration files:
 1. pg_hba.conf 
 2. postgresql.conf
  

(1) Open and modify pg_hba.conf file
>   sudo nano /etc/postgresql/9.4/main/pg_hba.conf

Allow all hosts from all IP's to connect to database by adding following line to the end of the file and save.
>   host all all 0.0.0.0/0 md5
    

(2) Open and modify postgresql.conf file 
>   sudo nano /etc/postgresql/9.4/main/postgresql.conf

Modify "peer" to "md5" on the line concerning postgres

| Original | Modified |
|----------| ---------|
| _local   all   postgres   peer_ | _local   all   postgres   md5_ | 

Restart the database
>   sudo /etc/init.d/postgresql restart

## <a name="3"><a/>3. Next steps

After these database configurations we can create a new database for social media data and necessary tables to store the data and control/manage the data collection process. 
[Continue and read the docs here.](pgdb_management.db)  