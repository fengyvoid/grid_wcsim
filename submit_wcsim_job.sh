RUN=$1
BATCH=$2

export INPUT_PATH=/pnfs/annie/scratch/users/doran/grid_wcsim_sample/                  

echo ""
echo "submitting job..."
echo ""

QUEUE=medium 

OUTPUT_FOLDER=/pnfs/annie/scratch/users/doran/output/wcsim/AmBe/${BATCH}
mkdir -p $OUTPUT_FOLDER                                                 

# wrapper script to submit your grid job
jobsub_submit --memory=2000MB --expected-lifetime=6h -G annie --disk=10GB --resource-provides=usage_model=OFFSITE --blacklist=Omaha,Swan,Wisconsin,SU-ITS,RAL -f ${INPUT_PATH}/WCSim.tar.gz -f ${INPUT_PATH}/wcsim_container.sh -d OUTPUT $OUTPUT_FOLDER file://${INPUT_PATH}/run_job.sh ${RUN} ${BATCH}

