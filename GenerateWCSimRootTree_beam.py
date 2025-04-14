#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import shutil
import subprocess

def main():

    # 1) Collect file IDs
    folder_path = "/pnfs/annie/scratch/users/yuefeng/WCSimOutput/BeamSimulation/beam_withInner/"
    WaitingForProcessing = []
    
    target_folder = "/pnfs/annie/persistent/users/yuefeng/WCSimResult_LAPPD/BeamSimulation/testFiles/"
    start_from = 0
    event_per_file = 2000

    # Store the path where this script was initially called
    original_path = os.getcwd()

    # Search for files in the given folder
    for filename in os.listdir(folder_path):
        if filename.startswith("wcsim_lappd.0.") and filename.endswith(".root"):
            # Extract the portion between "wcsim_mu_lappd_" and ".root"
            key_part = filename[len("wcsim_lappd.0.") : -len(".root")]
            WaitingForProcessing.append(key_part)
    
    WaitingForProcessing.sort()
    print("WaitingForProcessing list:", WaitingForProcessing)
    
    # wcsim_0.0.0.root
    # wcsim_lappd_0.0.0.root
    # wcsim_0.1.0.root,  wcsim_lappd.0.1.0.root


    total_files = len(WaitingForProcessing)
    for idx, file_id in enumerate(WaitingForProcessing, start=1):
        if idx < start_from:
            continue
        
        # extract the run number and sub run number from file_id
        # split the file_id by ., the first part is the run number, the second part is the sub run number
        run_number, sub_run_number = file_id.split('.')
        run_number = int(run_number)
        sub_run_number = int(sub_run_number)
        print(f"Processing {idx}/{total_files}: wcsim_lappd.0.{file_id}.root, file ID: {file_id} (Run: {run_number}, Sub-run: {sub_run_number})")


    #for file_id in WaitingForProcessing:
        config_path = os.path.join(original_path, "configfiles", "BeamClusterAnalysisMC")
        os.chdir(config_path)
        lappd_config_file = "LoadWCSimLAPPDConfig"
        if os.path.exists(lappd_config_file):
            with open(lappd_config_file, "r") as f:
                content_lappd = f.read()

            #pattern_lappd = r'^InputFile\s+.*/wcsim*\.root$'
            pattern_lappd = r'^InputFile\s+.*wcsim_lappd.*\.root$'

            replacement_lappd = f"InputFile {folder_path}wcsim_lappd.0.{file_id}.root"

            new_content_lappd = re.sub(
                pattern_lappd,
                replacement_lappd,
                content_lappd,
                flags=re.MULTILINE
            )
            if not re.search(pattern_lappd, content_lappd, flags=re.MULTILINE):
                print("[DEBUG] No match found in LoadWCSimLAPPDConfig!")


            with open(lappd_config_file, "w") as f:
                f.write(new_content_lappd)
        else:
            print(f"Warning: {lappd_config_file} not found. Skipping.")

        # -- 2.3) Modify LoadWCSimConfig
        # Similarly, we replace the entire line for 'wcsim_mu_*.root'.
        wcsim_config_file = "LoadWCSimConfig"
        if os.path.exists(wcsim_config_file):
            with open(wcsim_config_file, "r") as f:
                content_wcsim = f.read()

            #pattern_wcsim = r'^InputFile\s+.*wcsim*\.root$'
            pattern_wcsim = r'^InputFile\s+.*wcsim_0\..*\.root$'

            if not re.search(pattern_wcsim, content_wcsim, flags=re.MULTILINE):
                print("[DEBUG] No match found in LoadWCSimConfig!")
                
            replacement_wcsim = f"InputFile {folder_path}wcsim_0.{file_id}.root"

            new_content_wcsim = re.sub(
                pattern_wcsim,
                replacement_wcsim,
                content_wcsim,
                flags=re.MULTILINE
            )

            with open(wcsim_config_file, "w") as f:
                f.write(new_content_wcsim)
        else:
            print(f"Warning: {wcsim_config_file} not found. Skipping.")
            
            
        # -- 2.3.5) Modify LoadGenieConfig
        Genie_config_file = "LoadGenieEventConfig"
        if os.path.exists(Genie_config_file):
            with open(Genie_config_file, "r") as f:
                content_Genie = f.read()
                
            # FilePattern gntp.0.ghep.root
            # EventOffset 0
            offset = sub_run_number * event_per_file
            pattern_Genie = r'^FilePattern\s+gntp.*\.ghep\.root$'
            replacement_Genie = f"FilePattern gntp.{run_number}.ghep.root"
            
            pattern_offset = r'^EventOffset\s+\d+$'
            replacement_offset = f"EventOffset {offset}"
            new_content_Genie = re.sub(
                pattern_Genie,
                replacement_Genie,
                content_Genie,
                flags=re.MULTILINE
            )
            new_content_Genie = re.sub(
                pattern_offset,
                replacement_offset,
                new_content_Genie,
                flags=re.MULTILINE
            )
            with open(Genie_config_file, "w") as f:
                f.write(new_content_Genie)
        else:
            print(f"Warning: {Genie_config_file} not found. Skipping.")


        # -- 2.4) Change directory back to the original path
        os.chdir(original_path)

        # -- 2.5) Run the Analyse command
        subprocess.run(["./Analyse", "configfiles/BeamClusterAnalysisMC/ToolChainConfig"])

        # -- 2.6) Rename the output file ANNIETree_MC.root -> ANNIETree_MC_<file_id>.root
        old_file_name = "ANNIETree_MC.root"
        new_file_name = f"ANNIETree_MC_{file_id}.root"

        if os.path.exists(old_file_name):
            os.rename(old_file_name, new_file_name)
        else:
            print(f"Warning: {old_file_name} not found after running Analyse. Skipping rename for {file_id}.")
            continue

        # -- 2.7) Move the renamed file to WCSimRootTree folder, creating it if necessary
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        shutil.move(new_file_name, os.path.join(target_folder, new_file_name))

    print("All files processed successfully.")

if __name__ == "__main__":
    main()

