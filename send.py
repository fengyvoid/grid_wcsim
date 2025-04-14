import os,sys
import time
import subprocess
import glob


WCSim_loc = '/exp/annie/app/users/yuefeng/WCSimTools/devVersion/PrepareForGrid_beam/'
INPUT_PATH = '/pnfs/annie/persistent/users/yuefeng/WCSimResult_LAPPD/scripts_beam/'

genie_path = '/pnfs/annie/persistent/simulations/genie3/G1810a0211a/standardv1.0/tank/'
annieDirt_path = '/pnfs/annie/persistent/simulations/g4dirt/G1810a0211a/standardv1.0/tank/'

StartRunNumber = 0
submit_run_total = 1

job_label = 'beam_withInner_2000/'

####################
simEvent_per_job = 2000
####################

print('JobSetup: ')
print('Start to send WCSim jobs with beam sample.')
print('Total number of submited runs: ' + str(submit_run_total), ', using 20000 events per run.')
print('Each sub run job will have ' + str(simEvent_per_job) + ' events.')
print('Total number of events: ' + str(submit_run_total * 20000))
print('Total number of jobs: ' + str(submit_run_total * 20000 / simEvent_per_job))
print('The genie path is: ' + genie_path)
print('The annieDirt path is: ' + annieDirt_path)


print('\n')
print('Batch name: ' + job_label)
print('\n')

time.sleep(3)

WCSimMacro_path = WCSim_loc + 'WCSim/build/WCSim.mac'
with open(WCSimMacro_path, 'r') as file:
    lines = file.readlines()
with open(WCSimMacro_path, 'w') as file:
    for line in lines:
        if line.strip().startswith('/run/beamOn'):
            file.write(f'/run/beamOn {simEvent_per_job}\n')
            print("Change the number of events in WCSim.mac to: " + str(simEvent_per_job))
        else:
            file.write(line)
            
print('WCSim.mac details:')
print('------------------')
os.system('cat ' + WCSim_loc + 'WCSim/build/WCSim.mac')
print('\n')

time.sleep(3)

os.system('rm '+WCSim_loc+'WCSim/build/gntp.*.ghep.root')
os.system('rm '+WCSim_loc+'WCSim/build/annie_tank_flux.*.root')
os.system('rm '+WCSim_loc+'WCSim/build/wcsim_*')

os.system('rm -rf WCSim.tar.gz')   # remove old tar file
os.system('tar -czvf WCSim.tar.gz -C ' + WCSim_loc + ' WCSim')
time.sleep(1)     


print('\nSending jobs...\n')
submitted = 0
for run in range(submit_run_total):
    
    runNumber = int(StartRunNumber + run)
    genieFileName = genie_path + 'gntp.' + str(runNumber) + '.ghep.root'
    annieDirtFileName = annieDirt_path + 'annie_tank_flux.' + str(runNumber) + '.root'
      
    for subrun in range(int(20000/simEvent_per_job)):
        subrunNumber = int(subrun)
        runName = str(runNumber) + '_' + str(subrunNumber)


        primariesoffsetNumber = int(subrunNumber) * int(simEvent_per_job)

        print("Submitting " + str(submitted)+ "th job for run " + str(runNumber) + " subrun " + str(subrunNumber))
        os.system('sh submit_wcsim_job_beam.sh ' + runName + ' ' + job_label + ' ' + str(runNumber) + ' ' + str(subrunNumber) + ' ' + str(primariesoffsetNumber))
        submitted += 1



                
print('\nJobs sent\n')
print('Total jobs submitted: ' + str(submitted))

print('Jobs information:')
print('Start at run ' + str(StartRunNumber))
print('Total number of submited runs: ' + str(submit_run_total), ', using 20000 events per run.')
print('Each sub run job will have ' + str(simEvent_per_job) + ' events.')
print('Total number of events: ' + str(submit_run_total * 20000))
print('Total number of jobs: ' + str(submit_run_total * 20000 / simEvent_per_job))
print('The genie path is: ' + genie_path)
print('The annieDirt path is: ' + annieDirt_path)
