#!/usr/bin/env python
# coding: utf-8

# In[14]:


""""This script performs preprocessing of ECOG + LFP data."""
# Each script or module should have a brief description.

# Sort your imports: first python native libraries (like 'os' or 'json')
# .. then an empty line followed by 3rd party libraries that you have to
# .. install (for example mne, numpy etc.)
# .. and then your own modules. For example 'import maria_preprocessing.py'
# .. within these sections, I recommend to sort alphabetically
import os

from fooof import FOOOF
from fooof.plts.spectra import plot_spectrum, plot_spectra
import mne
import mne_bids
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import set_matplotlib_formats
import pandas as pd
import scipy
from scipy import stats


# Putting all executed code in a main function in each script helps you to
# avoid accidentally running some code when you for example import one of
# your scripts into a 2nd one of your scripts. You then run the main() function
# by using if __name__ == '__main__' .. (see bottom of script).
def main():
    """Main function of this script."""
    # defining PATHs
    RUN_NAME = (
        "sub-006_ses-EcogLfpMedOff01_task-Rest_acq-StimOff_run-1_ieeg.vhdr"
    )
    PATH_RUN = (
        "/Users/maria/Desktop/ECOG_LPF/sub-006/ses-EcogLfpMedOff01/ieeg/"
        + RUN_NAME
    )
    BIDS_PATH = "/Users/maria/Desktop/ECOG_LPF/"
    PATH_ANNOTATIONS = (
        BIDS_PATH + "artifact_annotation_task-Rest/sub-006/ses-EphysMedOff01/"
    )
    entities = mne_bids.get_entities_from_fname(PATH_RUN)
    bids_path = mne_bids.BIDSPath(
        subject=entities["subject"],
        session=entities["session"],
        task=entities["task"],
        run=entities["run"],
        acquisition=entities["acquisition"],
        datatype="ieeg",
        root=BIDS_PATH,
    )
    # loading the data as bids
    raw_arr = mne_bids.read_raw_bids(bids_path)
    
    # add annotations
    annot = mne.read_annotations(
        os.path.join(
            PATH_ANNOTATIONS,
            "artefact_detect_sub-006_ses-EphysMedOff01_task-Rest_acq-StimOff_run-01_ieeg"
            + ".csv",
        )
    )
    raw_arr = raw_arr.set_annotations(annot)
    
    #   """Preprocess data"""
    # picking only the ecog and dbs channels

    # A lot of methods of MNE Raw objects work "in-place"
    # .. this means that you don't need to write raw_arr = raw_arr...
    # each time, but you can just write raw_arr.method() and the
    # object will be modified in place. See below. If you are not sure if a
    # method works in-place or not (for example pandas DataFrame methods don't
    # work in-place), just try it out (or check the documentation for hints).
    
        # tmin, tmax = 0, 20  # use the first 20s of data
    tmin = 2
#     tmax = 180
    raw_arr = raw_arr.crop(tmin).load_data()
#     raw_arr.load_data(verbose=False)
    raw_arr.pick(picks=["ecog","dbs"], verbose=False)

# #     referencing ecog channels (bipolar)
#     raw_arr = mne.set_bipolar_reference(
#         raw_arr,
#         anode=[
#             "ECOG_R_01_SMC_AT",
#             "ECOG_R_02_SMC_AT",
#             "ECOG_R_03_SMC_AT",
#             "ECOG_R_04_SMC_AT",
#             "ECOG_R_05_SMC_AT",
#             "ECOG_R_06_SMC_AT",
#         ],
#         cathode=[
#             "ECOG_R_02_SMC_AT",
#             "ECOG_R_03_SMC_AT",
#             "ECOG_R_04_SMC_AT",
#             "ECOG_R_05_SMC_AT",
#             "ECOG_R_06_SMC_AT",
#             "ECOG_R_01_SMC_AT",
#         ],
#         ch_name=[
#             "ECOG_R_12",
#             "ECOG_R_23",
#             "ECOG_R_34",
#             "ECOG_R_45",
#             "ECOG_R_56",
#             "ECOG_R_61",
#         ],
#     )
    
    
#     raw_arr = mne.set_bipolar_reference(
#         raw_arr,
#         anode=[
#             "ECOG_L_01_SMC_AT",
#             "ECOG_L_02_SMC_AT",
#             "ECOG_L_03_SMC_AT",
#             "ECOG_L_04_SMC_AT",
#             "ECOG_L_05_SMC_AT",
#             "ECOG_L_06_SMC_AT",
#         ],
#         cathode=[
#             "ECOG_L_02_SMC_AT",
#             "ECOG_L_03_SMC_AT",
#             "ECOG_L_04_SMC_AT",
#             "ECOG_L_05_SMC_AT",
#             "ECOG_L_06_SMC_AT",
#             "ECOG_L_01_SMC_AT",
#         ],
#         ch_name=[
#             "ECOG_L_12",
#             "ECOG_L_23",
#             "ECOG_L_34",
#             "ECOG_L_45",
#             "ECOG_L_56",
#             "ECOG_L_61",
#         ],
#     )
        
    
    
#     # referencing LFP channels : bipolar with all bipolar montages
#     # setting R channels
    
#     anodes_right = [
#         "LFP_R_1_STN_MT",
#         "LFP_R_1_STN_MT",
#         "LFP_R_1_STN_MT",
#         "LFP_R_1_STN_MT",
#         "LFP_R_2_STN_MT",
#         "LFP_R_2_STN_MT",
#         "LFP_R_2_STN_MT",
#         "LFP_R_3_STN_MT",
#         "LFP_R_4_STN_MT",
#         "LFP_R_3_STN_MT",
#         "LFP_R_5_STN_MT",
#         "LFP_R_5_STN_MT",
#         "LFP_R_5_STN_MT",
#         "LFP_R_6_STN_MT",
#         "LFP_R_7_STN_MT",
#         "LFP_R_6_STN_MT"]
    
#     cathodes_right = [
#         "LFP_R_8_STN_MT",
#         "LFP_R_2_STN_MT",
#         "LFP_R_3_STN_MT",
#         "LFP_R_4_STN_MT",
#         "LFP_R_3_STN_MT",
#         "LFP_R_4_STN_MT",
#         "LFP_R_5_STN_MT",
#         "LFP_R_6_STN_MT",
#         "LFP_R_7_STN_MT",
#         "LFP_R_4_STN_MT",
#         "LFP_R_6_STN_MT",
#         "LFP_R_7_STN_MT",
#         "LFP_R_8_STN_MT",
#         "LFP_R_8_STN_MT",
#         "LFP_R_8_STN_MT",
#         "LFP_R_7_STN_MT"]
    
#     new_ch_names_right = [
#         "LFP_18_R_STN_MT",
#         "LFP_12_R_STN_MT",
#         "LFP_13_R_STN_MT",
#         "LFP_14_R_STN_MT",
#         "LFP_23_R_STN_MT",
#         "LFP_24_R_STN_MT",
#         "LFP_25_R_STN_MT",
#         "LFP_36_R_STN_MT",
#         "LFP_47_R_STN_MT",
#         "LFP_34_R_STN_MT",
#         "LFP_56_R_STN_MT",
#         "LFP_57_R_STN_MT",
#         "LFP_58_R_STN_MT",
#         "LFP_68_R_STN_MT",
#         "LFP_78_R_STN_MT",
#         "LFP_67_R_STN_MT"]
    
# #     # setting L channels

#     anodes_left = [ 
#         "LFP_L_8_STN_MT",
#         "LFP_L_2_STN_MT",
#         "LFP_L_3_STN_MT",
#         "LFP_L_4_STN_MT",
#         "LFP_L_2_STN_MT",
#         "LFP_L_2_STN_MT",
#         "LFP_L_2_STN_MT",
#         "LFP_L_3_STN_MT",
#         "LFP_L_4_STN_MT",
#         "LFP_L_3_STN_MT",
#         "LFP_L_5_STN_MT",
#         "LFP_L_5_STN_MT",
#         "LFP_L_5_STN_MT",
#         "LFP_L_6_STN_MT",
#         "LFP_L_7_STN_MT",
#         "LFP_L_6_STN_MT",
#     ]
    
#     cathodes_left = [
#         "LFP_L_1_STN_MT",
#         "LFP_L_1_STN_MT",
#         "LFP_L_1_STN_MT",
#         "LFP_L_1_STN_MT",
#         "LFP_L_3_STN_MT",
#         "LFP_L_4_STN_MT",
#         "LFP_L_5_STN_MT",
#         "LFP_L_6_STN_MT",
#         "LFP_L_7_STN_MT",
#         "LFP_L_4_STN_MT",
#         "LFP_L_6_STN_MT",
#         "LFP_L_7_STN_MT",
#         "LFP_L_8_STN_MT",
#         "LFP_L_8_STN_MT",
#         "LFP_L_8_STN_MT",
#         "LFP_L_7_STN_MT",
#     ]
    
#     new_ch_names_left = [
#         "LFP_18_L_STN_MT",
#         "LFP_12_L_STN_MT",
#         "LFP_13_L_STN_MT",
#         "LFP_14_L_STN_MT",
#         "LFP_23_L_STN_MT",
#         "LFP_24_L_STN_MT",
#         "LFP_25_L_STN_MT",
#         "LFP_36_L_STN_MT",
#         "LFP_47_L_STN_MT",
#         "LFP_34_L_STN_MT",
#         "LFP_56_L_STN_MT",
#         "LFP_57_L_STN_MT",
#         "LFP_58_L_STN_MT",
#         "LFP_68_L_STN_MT",
#         "LFP_78_L_STN_MT",
#         "LFP_67_L_STN_MT",
#     ]

#     anodes_right = [
#         "LFP_R_1_STN_BS",
#         "LFP_R_1_STN_BS",
#         "LFP_R_1_STN_BS",
#         "LFP_R_2_STN_BS",
#         "LFP_R_2_STN_BS",
#         "LFP_R_2_STN_BS",
#         "LFP_R_3_STN_BS",
#         "LFP_R_4_STN_BS",
#         "LFP_R_3_STN_BS",
#         "LFP_R_5_STN_BS",
#         "LFP_R_5_STN_BS",
#         "LFP_R_5_STN_BS",
#         "LFP_R_6_STN_BS",
#         "LFP_R_7_STN_BS",
#         "LFP_R_6_STN_BS",
#     ]
#     cathodes_right = [
#         "LFP_R_2_STN_BS",
#         "LFP_R_3_STN_BS",
#         "LFP_R_4_STN_BS",
#         "LFP_R_3_STN_BS",
#         "LFP_R_4_STN_BS",
#         "LFP_R_5_STN_BS",
#         "LFP_R_6_STN_BS",
#         "LFP_R_7_STN_BS",
#         "LFP_R_4_STN_BS",
#         "LFP_R_6_STN_BS",
#         "LFP_R_7_STN_BS",
#         "LFP_R_8_STN_BS",
#         "LFP_R_8_STN_BS",
#         "LFP_R_8_STN_BS",
#         "LFP_R_7_STN_BS",
#     ]
#     new_ch_names_right = [
#         "LFP_12_R_STN_BS",
#         "LFP_13_R_STN_BS",
#         "LFP_14_R_STN_BS",
#         "LFP_23_R_STN_BS",
#         "LFP_24_R_STN_BS",
#         "LFP_25_R_STN_BS",
#         "LFP_36_R_STN_BS",
#         "LFP_47_R_STN_BS",
#         "LFP_34_R_STN_BS",
#         "LFP_56_R_STN_BS",
#         "LFP_57_R_STN_BS",
#         "LFP_58_R_STN_BS",
#         "LFP_68_R_STN_BS",
#         "LFP_78_R_STN_BS",
#         "LFP_67_R_STN_BS",
#     ]
#     # setting L channels
#     anodes_left = [
#         "LFP_L_2_STN_BS",
#         "LFP_L_3_STN_BS",
#         "LFP_L_4_STN_BS",
#         "LFP_L_2_STN_BS",
#         "LFP_L_2_STN_BS",
#         "LFP_L_2_STN_BS",
#         "LFP_L_3_STN_BS",
#         "LFP_L_4_STN_BS",
#         "LFP_L_3_STN_BS",
#         "LFP_L_5_STN_BS",
#         "LFP_L_5_STN_BS",
#         "LFP_L_5_STN_BS",
#         "LFP_L_6_STN_BS",
#         "LFP_L_7_STN_BS",
#         "LFP_L_6_STN_BS",
#     ]
#     cathodes_left = [
#         "LFP_L_1_STN_BS",
#         "LFP_L_1_STN_BS",
#         "LFP_L_1_STN_BS",
#         "LFP_L_3_STN_BS",
#         "LFP_L_4_STN_BS",
#         "LFP_L_5_STN_BS",
#         "LFP_L_6_STN_BS",
#         "LFP_L_7_STN_BS",
#         "LFP_L_4_STN_BS",
#         "LFP_L_6_STN_BS",
#         "LFP_L_7_STN_BS",
#         "LFP_L_8_STN_BS",
#         "LFP_L_8_STN_BS",
#         "LFP_L_8_STN_BS",
#         "LFP_L_7_STN_BS",
#     ]
#     new_ch_names_left = [
#         "LFP_12_L_STN_BS",
#         "LFP_13_L_STN_BS",
#         "LFP_14_L_STN_BS",
#         "LFP_23_L_STN_BS",
#         "LFP_24_L_STN_BS",
#         "LFP_25_L_STN_BS",
#         "LFP_36_L_STN_BS",
#         "LFP_47_L_STN_BS",
#         "LFP_34_L_STN_BS",
#         "LFP_56_L_STN_BS",
#         "LFP_57_L_STN_BS",
#         "LFP_58_L_STN_BS",
#         "LFP_68_L_STN_BS",
#         "LFP_78_L_STN_BS",
#         "LFP_67_L_STN_BS",
#     ]

#     # doing re-referencing
#     anodes = anodes_right + anodes_left
#     cathodes = cathodes_right + cathodes_left
#     new_ch_names = new_ch_names_right + new_ch_names_left
#     raw_arr = mne.set_bipolar_reference(
#         raw_arr, anodes, cathodes, new_ch_names, drop_refs = True
#     )
    
#     raw_arr = raw_arr.reorder_channels(sorted(raw_arr.ch_names))
    
    raw_arr.pick_channels(
        ['LFP_R_1_STN_MT',
         'LFP_R_2_STN_MT',
         'LFP_R_3_STN_MT',
         'LFP_R_4_STN_MT',
         'LFP_R_5_STN_MT',
         'LFP_R_6_STN_MT',
         'LFP_R_7_STN_MT',
         'LFP_R_8_STN_MT',
        ])
        
        
#         "LFP_18_R_STN_MT",
#         "LFP_12_R_STN_MT",
# #         "LFP_13_R_STN_MT",
# #         "LFP_14_R_STN_MT",
#         "LFP_23_L_STN_MT",
# #         "LFP_24_L_STN_MT",
# #         "LFP_25_L_STN_MT",
# #         "LFP_36_L_STN_MT",
# #         "LFP_47_L_STN_MT",
#         "LFP_34_L_STN_MT",
#         "LFP_56_L_STN_MT",
# #         "LFP_57_L_STN_MT",
# #         "LFP_58_L_STN_MT",
# #         "LFP_68_L_STN_MT",
#         "LFP_78_L_STN_MT",
#         "LFP_67_L_STN_MT",
#     ])


    
    # PSD plotting parameters
    FMAX = 150
    TMIN = 2
    TMAX = 180
    PICKS = "dbs"
    fig, axs = plt.subplots(3, 1)
    raw_arr.plot_psd(
        fmax=FMAX,
        tmin=TMIN,
        tmax=TMAX,
        average=False,
        picks="dbs",
        ax=axs[0],
        show=False,
    )
    
    # applying notch filter
    line_freq = raw_arr.info["line_freq"]
    notch_freqs = np.arange(line_freq, raw_arr.info["sfreq"] * 0.5, line_freq)
    raw_arr = raw_arr.notch_filter(notch_freqs, picks="dbs")
    raw_arr.plot_psd(
        fmax=FMAX,
        tmin=TMIN,
        tmax=TMAX,
        average=False,
        picks="dbs",
        ax=axs[1],
        show=False,
    )
    
    # applying bandpass filter
    l_freq = 3
    # h_freq = 124
    raw_arr = raw_arr.filter(
        l_freq, 
        h_freq = None
    )

    # resampling
    resample_freq = 600
    raw_arr = raw_arr.resample(sfreq=resample_freq, verbose=False)
    raw_arr.plot_psd(
        fmax=FMAX,
        tmin=TMIN,
        tmax=TMAX,
        average=False,
        picks=PICKS,
        ax=axs[2],
        show=False,
    )

    axs[0].set_title("Before notch-filtering")
    axs[1].set_title("After notch-filtering, before resampling")
    axs[2].set_title("After notch-filtering and resampling")
    fig.tight_layout()
    set_matplotlib_formats('svg')
    plt.rcParams['savefig.dpi'] = 300
    plt.show(block=True)
    
    
    return raw_arr

# # Now the main function will be automatically executed if you run this script.
if __name__ == '__main__':
    raw_arr = main()   
