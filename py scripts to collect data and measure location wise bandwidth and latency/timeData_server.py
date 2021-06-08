import subprocess
from time import sleep
import datetime
import sys

## script parameters
result_file_S = "recordedTime_attServer.csv"
run_time_h = 24
interval_m = 15


## write the header row in the results file
print("Writing header... ", end="", flush=True)
csv_header_S = subprocess.check_output("./speedtest-cli --csv-header", shell=True)
with open("recordedTime.csv", "ab") as file:
    file.write(b"%s" % csv_header_S)
print("done")


## perform the measurement every interval_m for run_time_h
start_tm = datetime.datetime.now()
end_tm = start_tm + datetime.timedelta(hours=run_time_h)
print('Running from %s to %s' % (str(start_tm), str(end_tm)))

while datetime.datetime.now() < end_tm:
    run_tm = datetime.datetime.now()
    print("Starting run at %s... " % run_tm.strftime("%H:%M:%S"), end='', flush=True)
   
    csv_row_S=subprocess.check_output("./speedtest-cli --csv --server 5033", shell=True)
    with open("recordedTime_attServer.csv", "ab") as file:
        file.write(b"%s" % csv_row_S)
    print('recorded... ', end='', flush=True)

    sleep_td = run_tm \
            + datetime.timedelta(minutes=interval_m) \
            - datetime.datetime.now()
    sleep_s = sleep_td.total_seconds()
            
    print('sleeping for %ds... ' % sleep_s, end='', flush=True)
    sleep(sleep_s) 

    print("done")
