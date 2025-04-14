#!/bin/bash 
# James Minock 
# Modified by Steven Doran

PART_NAME=$1
runNumber=$2
subRunNumber=$3
offsetNumber=$4


# logfile
touch /srv/logfile_${PART_NAME}.txt 
echo "pwd:" >> /srv/logfile_${PART_NAME}.txt
pwd >> /srv/logfile_${PART_NAME}.txt
echo "" >> /srv/logfile_${PART_NAME}.txt

echo "sourcing script:" >> /srv/logfile_${PART_NAME}.txt
echo "" >> /srv/logfile_${PART_NAME}.txt

# source setup script
chmod +x sourceme
source sourceme >> /srv/logfile_${PART_NAME}.txt

mv genieFile/gntp.${runNumber}.ghep.root .
mv genieFile/annie_tank_flux.${runNumber}.root .

chmod +x update_offset.sh
./update_offset.sh ${offsetNumber}


cat WCSim.mac >> /srv/logfile_${PART_NAME}.txt
echo "" >> /srv/logfile_${PART_NAME}.txt

echo "running WCSim..." >> /srv/logfile_${PART_NAME}.txt

# Run the toolchain, and output verbose to log file 
chmod +x WCSim
./WCSim WCSim.mac >> /srv/logfile_${PART_NAME}.txt

echo "" >> /srv/logfile_${PART_NAME}.txt
echo "-----------------------------------------" >> /srv/logfile_${PART_NAME}.txt 
echo "Finished!" >> /srv/logfile_${PART_NAME}.txt :q

# log files
echo "" >> /srv/logfile_${PART_NAME}.txt
echo "WCSim directory contents:" >> /srv/logfile_${PART_NAME}.txt
ls -lrth >> /srv/logfile_${PART_NAME}.txt
echo "" >> /srv/logfile_${PART_NAME}.txt

cat macros/primaries_directory.mac >> /srv/logfile_${PART_NAME}.txt

# copy any produced files to /srv for extraction
cp wcsim_0.root /srv/wcsim_0.${runNumber}.${subRunNumber}.root 
cp wcsim_lappd_0.root /srv/wcsim_lappd.0.${runNumber}.${subRunNumber}.root

# make sure any output files you want to keep are put in /srv or any subdirectory of /srv 

### END ###
