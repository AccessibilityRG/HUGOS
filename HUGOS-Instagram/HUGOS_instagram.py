from instagram.client import InstagramAPI
import sys,time,datetime
from base import POSTGIS_DB_NAME, AWS_IP_ADDRESS, POSTGIS_PORT, POSTGIS_USERNAME, POSTGIS_PWD, INSTANCE_NAME, MONITOR_TABLE, CONTROL_TABLE, DATA_TABLE
import geopandas as gpd
import psycopg2
import pytz
import numpy as np

"""
-----------------
HUGOS-Instagram
-----------------

This tool is used for collecting HUGOS-Instagram data to PostGIS database.
Tool enables to collect data in a flexible way, i.e. it is possible to distribute the data collection to multiple servers.

Server connection details and database parameters are controlled and read from the base.py file.
Data collection is controlled and monitored using tables that are determined with MONITOR_TABLE and CONTROL_TABLE parameters in base.py.
Read the docs for further information and requirements.

Copyright (C) 2015  Accessibility Research Group (Tenkanen).
Developer: Henrikki Tenkanen, University of Helsinki, Finland.

--------------
License:
--------------

HUGOS-HUGOS-Instagram by Accessibility Research Group (University of Helsinki) is licensed under a Creative Commons Attribution 4.0 International License.
More information about license: http://creativecommons.org/licenses/by/4.0/
"""

def connect_to_DB(host, db_name, username, pwd, port):
    conn_string = "host='%s' dbname='%s' user='%s' password='%s' port='%s'" % (host, db_name, username, pwd, port)
    #print(conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    return(conn, cursor)

def track_progress_row(instance_name, shapefile, time, min_datetime, max_datetime):
    sql = "SELECT id FROM %s WHERE instance_name = '%s' AND input_shapefile = '%s' AND date(time) = '%s' AND min_time = '%s' AND max_time = '%s'" % (MONITOR_TABLE, instance_name, shapefile, time.date().isoformat(), min_datetime.isoformat(), max_datetime.isoformat())
    cursor.execute(sql)
    return cursor.fetchone()

def updateProgress(conn, instance_name, input_shape, min_datetime, max_datetime, index, start_position, end_position):
    # Update monitoring info
    current_time = datetime.datetime.now()
    progress_id = track_progress_row(instance_name, input_shape, current_time, min_datetime, max_datetime)
    # Calculate progress as percentage
    percentage = float(np.round((int(index)-int(start_position))/(int(end_position)-int(start_position)), 2))

    if not progress_id:
        insert_cmd = "INSERT INTO %s" % MONITOR_TABLE
        cursor.execute(insert_cmd + "(time, instance_name, min_time, max_time, current_status, end_position, percentage, total_rows, input_shapefile) \
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (current_time, instance_name, min_datetime, max_datetime, int(index), int(end_position), percentage, int(total_rows),  input_shape))
    else:
        cursor.execute("UPDATE %s SET time = '%s', current_status = %s, percentage = %s WHERE id = %s" % (MONITOR_TABLE, current_time, int(index), percentage, progress_id[0]))

    # Commit changes
    conn.commit()

def resetRestartIdx(conn, instance_name):
    restart_pos = 'NULL'
    cursor.execute("UPDATE %s SET restart_position = %s WHERE instance_name = '%s';" % (CONTROL_TABLE, restart_pos, instance_name))
    conn.commit()
    
###############################
# PARAMETERS
###############################

# PostGIS Authentication crecedentials
db_name, host, port, username, pwd = POSTGIS_DB_NAME, AWS_IP_ADDRESS, POSTGIS_PORT, POSTGIS_USERNAME, POSTGIS_PWD

# Create connection to Database
conn, cursor = connect_to_DB(host, db_name, username, pwd, port)

# Instance name of current server
instance_name = INSTANCE_NAME

# Get Parameters from database
sql = "SELECT input_shapefile, insta_client, insta_secret, min_time, max_time, search_radius, time_sequence, start_position, end_position, stop_at_end, commit_sequence, skip_time, restart_position FROM %s WHERE instance_name = '%s'" % (CONTROL_TABLE, instance_name)
cursor.execute(sql)
parameters = cursor.fetchall()[0]

# Set parameters to variables
fp = parameters[0]
client = parameters[1]
secret = parameters[2]
min_time = parameters[3]
max_time = parameters[4]
search_radius = parameters[5]
time_seq = parameters[6]
start_position = parameters[7]
end_position = parameters[8]
stop_at_end = parameters[9]
commit_seq = parameters[10]
skip_time = parameters[11]  # 3 weeks = 1814400 seconds
restart_idx = parameters[12]

###############################
# Program starts here ...
###############################

# API provides data back to xx days approximately (seems to provide data as long as there exists data)
low_limit = '2009-01-01T08:00:00'
lowest_unix = int(time.mktime(datetime.datetime.strptime(low_limit, "%Y-%m-%dT%H:%M:%S").timetuple()))

# Authenticate HUGOS-Instagram
api = InstagramAPI(client_id=client, client_secret=secret)

# Read hexagon points
data = gpd.read_file(fp)
total_rows = data.index.max()
input_shape = fp

# Create Unix times from timestamps
min_unix = int(time.mktime(datetime.datetime.strptime(min_time, "%Y-%m-%dT%H:%M:%S").timetuple()))
max_unix = int(time.mktime(datetime.datetime.strptime(max_time, "%Y-%m-%dT%H:%M:%S").timetuple()))  

# Parse datetime objects from unix time
min_datetime = datetime.datetime.fromtimestamp(min_unix)
max_datetime = datetime.datetime.fromtimestamp(max_unix)

# Check if collection was restarted
orig_start_position = start_position
if restart_idx > 0:
    start_position = restart_idx

while True:
    if min_unix >= lowest_unix:

        #Print information about time-interval
        print("Min_timestamp: ", min_datetime, " Max_timestamp: ", max_datetime)
        
        #--------------------------------------
        # Search media 
        #--------------------------------------
                
        # Commit index
        commit_i = 0
                
        for index, row in data.iterrows():
            
            # A handler to skip input locations by index
            if index >= start_position:
                start = time.time()

                # Get coordinates
                longitude = row['geometry'].x
                latitude = row['geometry'].y
                place_id = row['place_id']
                hex_id = row['hex_id']

                # Print some info
                print(index, " ", latitude, " ", longitude)

                # If timezone is 'uninhabited' (e.g. areas near South-pole) set GMT timezone
                if row['timezone'] == 'uninhabited':
                    local_tz = pytz.timezone('GMT')
                else:
                    local_tz = pytz.timezone(row['timezone'])

                # Fetch data from HUGOS-Instagram API
                try:
                    search_result = api.media_search(lat=latitude, lng=longitude,min_timestamp=min_unix, max_timestamp=max_unix, distance=search_radius, count=200) 

                    for media in search_result:
                        if media.caption:
                            if 'bio' in media.user.__dict__.keys():
                                bio = media.user.bio
                            else:
                                bio = ''

                            latitude, longitude, coords, userid, username, fullname, photourl, photoid, likes = media.location.point.latitude, media.location.point.longitude, "POINT(%s %s)" % (longitude, latitude), media.user.id, media.user.username, media.user.full_name, media.images['standard_resolution'].url, media.id, media.like_count
                                                          
                            # Convert UTC time to local time
                            utc_time, utc_timezone = media.created_time, pytz.utc.localize(media.created_time)
                            local_time = utc_timezone.astimezone(local_tz).isoformat()

                            text, medialink = media.caption.text, media.link

                            insert_cmd = "INSERT INTO %s" % DATA_TABLE
                            cursor.execute(insert_cmd + "(userid, username, fullname, text, time_utc, time_local, latitude, longitude, geom, likes, photourl, photoid, medialink, bio, place_id, hex_id) \
                                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326), %s, %s, %s, %s, %s, %s, %s)",
                                           (userid, username, fullname, text, utc_time, local_time, latitude, longitude, coords, likes,
                                            photourl, photoid, medialink, bio, place_id, hex_id))

                    # Update commit index
                    commit_i += 1

                    # Commit changes to db according with interval determined in 'commit_seq' parameter
                    if not commit_i < commit_seq:
                        conn.commit()

                        print("\n--------Committed changes--------\n")

                        # Reset commit index
                        commit_i = 0

                        # Update progress monitor
                        updateProgress(conn, instance_name, input_shape, min_datetime, max_datetime, index, start_position, end_position)

                except Exception as e:
                    print(e)

                    #Print information about time-interval
                    print("Min_timestamp: ", datetime.datetime.fromtimestamp(min_unix), " Max_timestamp: ", datetime.datetime.fromtimestamp(max_unix))

                    if "UnicodeDecodeError" in str(type(e)):
                        pass
                    elif "ResponseNotReady" in str(type(e)):
                        time.sleep(10)
                        pass
                    elif 'Unable to find the server' in str(type(e)):
                        time.sleep(60*5)
                        pass
                    elif "request per second" in e.error_message:
                        time.sleep(60*10)
                        pass
                    elif "not valid JSON" in e.error_message:
                        pass
                    elif "object has no attribute 'location'" in e.error_message:
                        pass
                    elif "missing lat and lng" in e.error_message:
                        pass
                    else:
                        raise e

                end = time.time()
                duration = end-start

                # Need to sleep awhile for not exceeding the rate limit (max 5000 requests per hour --> 1 request per 1.38 seconds)
                if duration < 1.5:
                    time.sleep(1.5-duration)
                    print(1.5)
                else:
                    print(duration)

                # Check if user wants to stop iteration
                if int(index) == end_position:
                    if stop_at_end:
                        print("End position (%s) reached..Committing changes and stopping program..." % index)
                        conn.commit()

                        # Update progress monitor
                        updateProgress(conn, instance_name, input_shape, min_datetime, max_datetime, index, start_position, end_position)

                        cursor.close()
                        conn.close()
                        sys.exit()
                    else:
                        # If collection was restarted using 'restart_position' update start position to original start_position
                        if restart_idx > 0:
                            start_position = orig_start_position
                            # Set restart index to None
                            resetRestartIdx(conn, instance_name)
                        break
            else:
                pass

        #Update time-intervals (+ additional skip time if wanted)
        min_unix = max_unix + skip_time
        max_unix = max_unix + time_seq + skip_time

        # Parse datetime objects from unix time
        min_datetime = datetime.datetime.fromtimestamp(min_unix)
        max_datetime = datetime.datetime.fromtimestamp(max_unix)

    else:
        cursor.close()
        conn.close()
        #End loop
        sys.exit()
