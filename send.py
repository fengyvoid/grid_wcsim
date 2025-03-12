import os,sys
import time


WCSim_loc = '/exp/annie/app/users/yuefeng/WCSimTools/devVersion/PrepareForGrid/'
INPUT_PATH = '/pnfs/annie/persistent/users/yuefeng/WCSimResult_LAPPD/scripts/'

job_label = 'muon_grid_withInner_10cmStepSize/'
####################
events_per_job = 1000                 # same as in the WCSim.mac file
####################

#### new parameters to specify muon position looping
#### generate muon gun events for different position and direction
#/gun/direction -0.4 0 0.6
#/gun/position 500 -144 1200 mm
# need to change this in the WCSim.mac in build folder
MuDirectionOrigion = [0, 0, 1]
MuPositionOrigion = [0, -144, 1681]
#MuXStepNumber = 7 # 2n + 1 step on x direction
#MuXStepSize = 30 # 3 cm
#MuYStepNumber = 7 # 2n + 1 step on y direction
#MuYStepSize = 30 # 3 cm

MuXStepNumber = 1 # 2n + 1 step on x direction
MuXStepSize = 100 # 3 cm
MuYStepNumber = 1 # 2n + 1 step on y direction
MuYStepSize = 100 

MuXDirectionStepSize = 0.1
MuXDirectionStepNumber = 1  # 2n+1 steps in total
MuYDirectionStepSize = 0.2
MuYDirectionStepNumber = 1 # 2n+1 steps in total

TotalStepNumber = (MuXStepNumber*2+1) * (MuYStepNumber*2+1) * (MuXDirectionStepNumber*2+1) * (MuYDirectionStepNumber*2+1)
total_events = TotalStepNumber * events_per_job


print('JobSetup: ')
print('Loop muon gun position and direction:')
print('The center of the grid is at ',MuPositionOrigion)
print('The grid step on X direction is ' + str(MuXStepNumber) + ' with step size = ' + str(MuXStepSize) + ' mm')
print('The grid step on Y direction is ' + str(MuYStepNumber) + ' with step size = ' + str(MuYStepSize) + ' mm')
print('Also changing the muon direction horizontaly and vertically')
print('The step size on X direction is ' + str(MuXDirectionStepSize) + ' with ' + str(MuXDirectionStepNumber) + ' steps')
print('The step size on Y direction is ' + str(MuYDirectionStepSize) + ' with ' + str(MuYDirectionStepNumber) + ' steps')
print('Total number of jobs: ' + str(TotalStepNumber))
print('Total number of events: ' + str(TotalStepNumber * events_per_job))
print('!!!! You need to set those step size in modify.sh')


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


txt_filename = "/pnfs/annie/persistent/users/yuefeng/WCSimResult_LAPPD/scripts/waitingforsubmit.txt"

run_names_in_txt = set()

with open(txt_filename, 'r') as f:
    for line in f:
        tokens = line.strip().split()
        if "run_job.sh" in tokens:
            idx = tokens.index("run_job.sh")
            if idx + 1 < len(tokens):
                run_name_from_line = tokens[idx+1]
                run_names_in_txt.add(run_name_from_line)

print('Finding unprocessed runName', run_names_in_txt)


print('\nSending jobs...\n')


submitted = 0
for xStep in range(-MuXStepNumber, MuXStepNumber + 1):
    for yStep in range(-MuYStepNumber, MuYStepNumber + 1):
        for xDirectionStep in range(-MuXDirectionStepNumber, MuXDirectionStepNumber + 1):
            for yDirectionStep in range(-MuYDirectionStepNumber, MuYDirectionStepNumber + 1):
                print(xStep, yStep, xDirectionStep, yDirectionStep)
                runName = 'x' + str(xStep) + '_y' + str(yStep) + '_dirx' + str(xDirectionStep) + '_diry' + str(yDirectionStep)
                #if runName not in run_names_in_txt:
                #    continue
                #else:
                print("Submitting " + str(submitted)+ "th job for " + runName)
                os.system('sh submit_wcsim_job.sh ' + runName + ' ' + job_label + ' ' + str(xStep) + ' ' + str(yStep) + ' ' + str(xDirectionStep) + ' ' + str(yDirectionStep))
                submitted += 1
                          
                
print('\nJobs sent\n')
print('Total jobs submitted: ' + str(submitted))
