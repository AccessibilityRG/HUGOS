# Postgres/PostGIS configurations

In this document we:

1. [Create a new user for Postgresql database](#1)
2. [Open the server (database) to 'listen' the world (i.e. enable other servers/computers to insert data to our database)](#2).

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
 1. postgresql.conf
 2. pg_hba.conf

Open and modify pg_hba.conf file
>   sudo nano /etc/postgresql/9.4/main/pg_hba.conf
    
Modify "peer" to "md5" on the line concerning postgres
| Original | Modified |
|----------| ---------|
|>   local   all   postgres   peer | >   local   all   postgres   md5 


>   sudo service postgresql restart


Modify pg_hba.conf again and change peer to md5
>   sudo nano /etc/postgresql/9.4/main/pg_hba.conf
     local      all     all     peer md5

Restart the database again
>   sudo /etc/init.d/postgresql restart


