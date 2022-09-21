
from mne.datasets.fieldtrip_cmc import data_path
from mne.decoding import SSD

freqs_sig = 8, 12
freqs_noise = 7, 13

ssd_raw = SSD(info=raw_arr.info,
#               reg='oas',
#               sort_by_spectral_ratio=True,
              filt_params_signal=dict(l_freq=freqs_sig[0], h_freq=freqs_sig[1],
                                        l_trans_bandwidth=1, h_trans_bandwidth=1),
              filt_params_noise=dict(l_freq=freqs_noise[0], h_freq=freqs_noise[1],
                                       l_trans_bandwidth=1, h_trans_bandwidth=1),
#               rank = 'info'
                )
                                          
ssd_raw.fit(X=raw_arr.get_data())

# Transform
ssd_sources = ssd_raw.transform(X=raw_arr.get_data())

#setting parameters for tfr_morlet
decim = 2 #default  = 1
freqs_wv = np.arange(3, 50, 1)  # define frequencies of interest- beta region
n_cycles = 7
sfreq = raw_arr.info["sfreq"]

# Get psd of SSD-filtered signals.
psd, freqs = mne.time_frequency.psd_array_welch(
    ssd_sources, sfreq, fmin=3, fmax=50, n_fft = 512)


# Get spec_ratio information (already sorted).
# Note that this is not necessary if sort_by_spectral_ratio=True (default).
spec_ratio, sorter = ssd_raw.get_spectral_ratio(ssd_sources)

# Plot spectral ratio (see Eq. 24 in Nikulin 2011).
fig, ax = plt.subplots(1)
ax.plot(spec_ratio, color='black')
ax.plot(spec_ratio[sorter], color='orange', label='sorted eigenvalues')
ax.set_xlabel("Eigenvalue Index")
ax.set_ylabel(r"Spectral Ratio $\frac{P_f}{P_{sf}}$")
ax.legend()
ax.axhline(1, linestyle='--')


### plotting psds for different channels to choose the one with highest peak power
psd_db = 10 * np.log10(psd)

f, ax = plt.subplots()
for idx, val in enumerate(psd_db[:,0]):
    ax.plot(freqs, psd_db[idx, :])   #epoch1
    ax.set(xlim = [3,50], title = 'Psd for LFP Right channels with SSD', xlabel='Frequency (Hz)',
           ylabel='Power Spectral Density (dB)')
# ax.set_xscale('log')
# ax.legend([raw_arr.ch_names[0],raw_arr.ch_names[1],raw_arr.ch_names[2],raw_arr.ch_names[3]])
set_matplotlib_formats('svg')
# plt.savefig('18_LFP_R_STN_MT_SSD.png', bbox_inches='tight')
plt.show()

#now apply the filters 
freqs_sig = 8, 12
freqs_noise = 7, 13

ssd_alpha = SSD(info=raw_arr.info,
#               reg='oas',
#               sort_by_spectral_ratio=True,
              filt_params_signal=dict(l_freq=freqs_sig[0], h_freq=freqs_sig[1],
                                        l_trans_bandwidth=1, h_trans_bandwidth=1),
              filt_params_noise=dict(l_freq=freqs_noise[0], h_freq=freqs_noise[1],
                                       l_trans_bandwidth=1, h_trans_bandwidth=1),
                n_components = 2,
#               rank = 'info'
                )
                                          
ssd_sources_alpha = ssd_alpha.fit(X=raw_arr.get_data())


# Apply
raw_filtered_alpha = ssd_alpha.apply(X=raw_arr.get_data())

#setting parameters for filered psd
decim = 2 #default  = 1
freqs_wv = np.arange(3, 50, 1)  # define frequencies of interest- beta region
n_cycles = 7
sfreq = raw_arr.info["sfreq"]

# Get psd of SSD-filtered signals.
psd_filtered, freqs = mne.time_frequency.psd_array_welch(
    raw_filtered_alpha, sfreq, fmin=3, fmax=50, n_fft = 512)


### plotting psds for different channels to choose the one with highest peak power
psd_filtered_db = 10 * np.log10(psd_filtered)

f, ax = plt.subplots()
for idx, val in enumerate(psd_filtered_db[:,0]):
    ax.plot(freqs, psd_filtered_db[idx, :])   #epoch1
    ax.set(xlim = [3,50], title = 'Psd for LFP Right channels filtered', xlabel='Frequency (Hz)',
           ylabel='Power Spectral Density (dB)')
# ax.set_xscale('log')
# ax.legend([raw_arr.ch_names[0],raw_arr.ch_names[1],raw_arr.ch_names[2],raw_arr.ch_names[3]])
set_matplotlib_formats('svg')
# plt.savefig('18_LFP_R_STN_MT_SSD.png', bbox_inches='tight')
plt.show()

#plottong PSD for unfiltered data
raw_data = raw_arr.get_data()

#setting parameters for tfr_morlet
decim = 2 #default  = 1
freqs_wv = np.arange(3, 50, 1)  # define frequencies of interest- beta region
n_cycles = 7
sfreq = raw_arr.info["sfreq"]

# Get psd of SSD-filtered signals.
psd_raw, freqs = mne.time_frequency.psd_array_welch(
    raw_data, sfreq, fmin=3, fmax=50, n_fft = 512)


### plotting psds for different channels to choose the one with highest peak power
psd_raw_db = 10 * np.log10(psd_raw)

f, ax = plt.subplots()
for idx, val in enumerate(psd_raw_db[:,0]):
    ax.plot(freqs, psd_raw_db[idx, :])   #epoch1
    ax.set(xlim = [3,50], title = 'Psd for LFP Right channels raw', xlabel='Frequency (Hz)',
           ylabel='Power Spectral Density (dB)')
# ax.set_xscale('log')
# ax.legend([raw_arr.ch_names[0],raw_arr.ch_names[1],raw_arr.ch_names[2],raw_arr.ch_names[3]])
set_matplotlib_formats('svg')
# plt.savefig('18_LFP_R_STN_MT_SSD.png', bbox_inches='tight')
plt.show()
