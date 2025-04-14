RUN=$1
BATCH=$2
RUNNumber=$3
SUBRUNNumber=$4


export INPUT_PATH=/pnfs/annie/persistent/users/yuefeng/WCSimResult_LAPPD/scripts_beam/                  

echo ""
echo "submitting job..."
echo ""

QUEUE=medium 

OUTPUT_FOLDER=/pnfs/annie/scratch/users/yuefeng/WCSimOutput/BeamSimulation/${BATCH}
mkdir -p $OUTPUT_FOLDER                                                 

# wrapper script to submit your grid job
jobsub_submit --memory=4000MB --expected-lifetime=8h -G annie --disk=8GB --resource-provides=usage_model=OFFSITE --blacklist=Omaha,Swan,Wisconsin,SU-ITS,RAL -f ${INPUT_PATH}/WCSim.tar.gz -f ${INPUT_PATH}/wcsim_container.sh -d OUTPUT $OUTPUT_FOLDER file://${INPUT_PATH}/run_job.sh ${RUN} ${RUNNumber} ${SUBRUNNumber} 

