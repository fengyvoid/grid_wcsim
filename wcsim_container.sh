#!/bin/bash 
# James Minock 
# Modified by Steven Doran

PART_NAME=$1


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


# change the WCSim.mac file
chmod +x modifyMac.sh
source modifyMac.sh $2 $3 $4 $5 >> /srv/logfile_${PART_NAME}.txt

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

# copy any produced files to /srv for extraction
cp wcsim_mu_0.root /srv/wcsim_mu_${PART_NAME}.root 
cp wcsim_mu_lappd_0.root /srv/wcsim_mu_lappd_${PART_NAME}.root

# make sure any output files you want to keep are put in /srv or any subdirectory of /srv 

### END ###
