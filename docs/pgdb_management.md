# PostGIS database management

**Create a new postgresql database named 'socialmedia'**
>   createdb socialmedia --encoding='utf8'

**Start psql and log into the database**
>   $psql -U myUserName socialmedia

**Set-up PostGIS extensions**
>   # CREATE EXTENSION postgis;
>   # CREATE EXTENSION postgis_topology;

**Create table for controlling the data collection**
> CREATE TABLE process_control(

>  id serial PRIMARY KEY,

>  instance_name TEXT,

>  input_shapefile TEXT,

>  insta_client TEXT,

>  insta_secret TEXT,

>  min_time TEXT,

>  max_time TEXT,

>  search_radius INTEGER,

>  time_sequence INTEGER,

>  start_position INTEGER,
>  end_position INTEGER,
>  stop_at_end BOOLEAN,
>  commit_sequence INTEGER,
>  skip_time INTEGER,
>  restart_position INTEGER
>  );

Create a table for monitoring

CREATE TABLE progress_monitor(
   id serial PRIMARY KEY,
   time TIMESTAMP WITH TIME ZONE NOT NULL,
   instance_name TEXT,  
   min_time timestamp,
   max_time timestamp,
   current_status INTEGER,
   end_position INTEGER,
   percentage DECIMAL,
   total_rows INTEGER,
   input_shapefile TEXT
   );