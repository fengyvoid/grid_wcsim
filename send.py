import os,sys
import time

WCSim_loc = '/exp/annie/app/users/doran/grid_wcsim/'
INPUT_PATH = '/pnfs/annie/scratch/users/doran/grid_wcsim/'

job_label = 'AmBe_port5_zminus100/'        # This will also serve as the embedded output folder

####################
events_per_job = 1000                 # same as in the WCSim.mac file
####################
N_jobs = 25
####################
total_events = int(N_jobs*events_per_job)

print('\nYou have chosen:\n')
print(' - ' + str(events_per_job) + ' events per job\n')
print(' - ' + str(N_jobs) + ' total jobs to be submitted\n')
print(' - ' + str(total_events) + ' total events across all jobs\n')
print('\n')
print('Batch name: ' + job_label)
print('\n')

time.sleep(3)

print('WCSim.mac details:')
print('------------------')
os.system('cat ' + WCSim_loc + 'WCSim/build/WCSim.mac')
print('\n')

time.sleep(5)

# tar WCSim
print('\ntar-ing WCSim for grid submission...\n')
os.system('rm -rf WCSim.tar.gz')   # remove old tar file
os.system('cd ' + WCSim_loc)
os.system('tar -czvf WCSim.tar.gz -C ' + WCSim_loc + ' WCSim')
time.sleep(1)


print('\nSending jobs...\n')
for i in range(N_jobs):
    starting_event = i*events_per_job
    ending_event = (i+1)*events_per_job - 1
    print('\n########## ' + str(starting_event) + '_' + str(ending_event) + ' ###########\n')
    os.system('sh submit_wcsim_job.sh ' + str(starting_event) + '_' + str(ending_event) + ' ' + job_label)


print('\nJobs sent\n')
