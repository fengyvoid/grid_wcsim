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

#create a tmp folder to store the tar file if it does not exist
if not os.path.exists('tmp'):
    os.makedirs('tmp')
    print('Create tmp folder to store the tar file.\n')

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

print('Setting up ifdh cp...\n')
#subprocess.run('source /cvmfs/fermilab.opensciencegrid.org/products/common/etc/setup && setup ifdhc v2_5_4', shell=True, executable='/bin/bash')
#os.system('source /cvmfs/fermilab.opensciencegrid.org/products/common/etc/setup')
#os.system('setup ifdhc v2_5_4')

print('\nSending jobs...\n')
submitted = 0
for run in range(submit_run_total):
    
    runNumber = int(StartRunNumber + run)
    genieFileName = genie_path + 'gntp.' + str(runNumber) + '.ghep.root'
    annieDirtFileName = annieDirt_path + 'annie_tank_flux.' + str(runNumber) + '.root'
    
    # remove any old files
    for file in glob.glob(os.path.join(WCSim_loc, 'WCSim/build/gntp*.root')):
        subprocess.run(['rm', '-f', file])
    for file in glob.glob(os.path.join(WCSim_loc, 'WCSim/build/annie_tank_flux*.root')):
        subprocess.run(['rm', '-f', file])
    for file in glob.glob(os.path.join(WCSim_loc, 'WCSim/build/wcsim_*.root')):
        subprocess.run(['rm', '-f', file])
        
    # copy files to WCSim location
    os.system('cp ' + genieFileName + ' ' + WCSim_loc + 'WCSim/build/.')
    os.system('cp ' + annieDirtFileName + ' ' + WCSim_loc + 'WCSim/build/.')
    #subprocess.run(['ifdh', 'cp', genieFileName, WCSim_loc + 'WCSim/build/.'], shell=True, executable='/bin/bash', check=True)
    #subprocess.run(['ifdh', 'cp', annieDirtFileName, WCSim_loc + 'WCSim/build/.'], shell=True, executable='/bin/bash', check=True)
            
    for subrun in range(int(20000/simEvent_per_job)):
        subrunNumber = int(subrun)
        runName = str(runNumber) + '_' + str(subrunNumber)

        # modify macros
        primariesoffsetNumber = int(subrunNumber) * int(simEvent_per_job)
        macro_path = WCSim_loc + 'WCSim/build/macros/primaries_directory.mac'
        with open(macro_path, 'r') as file:
            lines = file.readlines()
        with open(macro_path, 'w') as file:
            for line in lines:
                if line.strip().startswith('/mygen/primariesoffset'):
                    file.write(f'/mygen/primariesoffset {primariesoffsetNumber}\n')
                    print("Change the primariesoffset to: " + str(primariesoffsetNumber))
                else:
                    file.write(line)
                    
        # tar WCSim directory
        print('\ntar-ing WCSim for grid submission...\n')
        os.system('tar -czvf tmp/WCSim.tar.gz -C ' + WCSim_loc + ' WCSim')
        time.sleep(10)     
        os.system('rm -rf WCSim.tar.gz')   # remove old tar file
        os.system('mv tmp/WCSim.tar.gz .')

        print("Submitting " + str(submitted)+ "th job for run " + str(runNumber) + " subrun " + str(subrunNumber) + " with genie file: " + genieFileName)
        os.system('sh submit_wcsim_job_beam.sh ' + runName + ' ' + job_label + ' ' + str(runNumber) + ' ' + str(subrunNumber) )
        submitted += 1

        time.sleep(10)


                
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
