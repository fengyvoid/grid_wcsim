RUN=$1
BATCH=$2
xStep=$3
yStep=$4
xDirStep=$5
yDirStep=$6

export INPUT_PATH=/pnfs/annie/persistent/users/yuefeng/WCSimResult_LAPPD/scripts/                  

echo ""
echo "submitting job..."
echo ""

QUEUE=medium 

OUTPUT_FOLDER=/pnfs/annie/scratch/users/yuefeng/WCSimOutput/MuonMapping/${BATCH}
mkdir -p $OUTPUT_FOLDER                                                 

# wrapper script to submit your grid job
jobsub_submit --memory=2000MB --expected-lifetime=12h -G annie --disk=10GB --resource-provides=usage_model=OFFSITE --blacklist=Omaha,Swan,Wisconsin,SU-ITS,RAL -f ${INPUT_PATH}/WCSim.tar.gz -f ${INPUT_PATH}/wcsim_container.sh -d OUTPUT $OUTPUT_FOLDER file://${INPUT_PATH}/run_job.sh ${RUN} ${BATCH} ${xStep} ${yStep} ${xDirStep} ${yDirStep}

