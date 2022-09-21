#fooof for epoched data
results = []
periodic_STN_alpha = []
periodic_STN_low_beta = []
periodic_STN_beta = []
periodic_STN = []
fooofed_STN_per = []
periodic_STN_err = []
freq_range = [3,50]

#creating a loop over all epochs for STN electrode and saving to df
for idx, val in enumerate(avpower_lfp_R_beta[:,0]):
    #creating fooof object and performing the fitting
    fm = FOOOF(peak_width_limits=(0.08, 20.0), min_peak_height=0.01, aperiodic_mode='fixed', max_n_peaks=3)
    fm.report(freqs_wv, avpower_lfp_R_beta[idx,:],freq_range,plt_log=True)  #epoch 1

    cfs = fm.get_params('peak_params', 'CF')
    pws = fm.get_params('peak_params', 'PW')
    bws = fm.get_params('peak_params', 'BW')
    r_sq = fm.get_params('r_squared')
    
     
    cfs = np.array(cfs, ndmin = 1)
    pws = np.array(pws, ndmin = 1)
    bws = np.array(bws, ndmin = 1)
    
    # making list with alpha band peak properties
    list = []
    list_alpha = []
    list_low_beta = []
    list_beta = []
    for i in range(len(cfs)):
        if cfs[i] > 8 and cfs[i] < 12:

            list_alpha = (cfs[i], pws[i], bws[i])
            periodic_STN_alpha.append(list_alpha)
            
        if cfs[i] > 12 and cfs[i] < 20:
            list_low_beta = (cfs[i], pws[i], bws[i])
            periodic_STN_low_beta.append(list_low_beta)
            
        if cfs[i] > 20 and cfs[i] < 35:
            list_beta = (cfs[i], pws[i], bws[i])
            periodic_STN_beta.append(list_beta)
    
        list = (list_alpha, list_low_beta, list_beta)
    results.append(list)
  
        
#     # saving aperiodic + periodic parameters to a list appending over all epochs
    list = (cfs, pws, bws)
#     list = (exp, offset, knee, cfs, pws, bws, err, r_sq)
    periodic_STN.append(list)
    
    
    #saving fooofed spectra for all events as a list
    list1 = (fm.fooofed_spectrum_)
    fooofed_STN_per.append(list1)
    
    #saving error
    list2 = (r_sq)
    periodic_STN_err.append(list2)
    

column_names_full = ["Central frequency STN", "Peak power STN", "Band width STN"]
column_error = ["R_squared STN Periodic"]

df_periodic_STN_peaks = pd.DataFrame(periodic_STN, columns = column_names_full)  
df_periodic_STN = pd.DataFrame(results, columns = column_names_full)  
df_periodic_STN_err = pd.DataFrame(periodic_STN_err, columns = column_error)    
    


#expanding multiple peaks into separate columns and renaming them
stn = df_periodic_STN.apply(lambda x: pd.Series(x['Central frequency STN']),axis=1,result_type='expand')
stn = df_periodic_STN.drop('Central frequency STN', axis=1).join(stn)
stn = stn.rename(columns={0: 'CF alpha STN', 1: 'Ampl alpha STN', 2: 'BW alpha STN'})
pw = df_periodic_STN.apply(lambda x: pd.Series(x['Peak power STN']),axis=1,result_type='expand')
stn = stn.drop('Peak power STN', axis=1).join(pw)
stn = stn.rename(columns={0: 'CF low beta STN', 1: 'Ampl low beta STN', 2: 'BW low beta STN'})
bw = df_periodic_STN.apply(lambda x: pd.Series(x['Band width STN']),axis=1,result_type='expand')
stn = stn.drop('Band width STN', axis=1).join(bw)
stn = stn.rename(columns={0: 'CF high beta STN', 1: 'Ampl beta STN', 2: 'BW beta STN'})



#FOOOF STN
#fooof for epoched data
aperiodic_STN = []
aperiodic_STN_err = []
fooofed_STN = []
freq_range = [35,70]

#creating a loop over all epochs for STN electrode and saving to df
for idx, val in enumerate(avpower_lfp_R_beta[:,0]):
    print(idx)
    #creating fooof object and performing the fitting
    fm = FOOOF(peak_width_limits=(0.5, 15.0), min_peak_height=0.1, aperiodic_mode='fixed', max_n_peaks=1)
    fm.report(freqs_wv, avpower_lfp_R_beta[idx,:],freq_range,plt_log=False)  #epoch 1
#     fm.plot(plot_aperiodic=False, save_fig = True, file_name = filename + str(idx), add_legend = True) #('test.png', bbox_inches='tight')
    
    # Extract a model parameter with `get_params`
#     err = fm.get_params('error')
    exp = fm.get_params('aperiodic_params', 'exponent')
    offset = fm.get_params('aperiodic_params', 'offset')
#     knee = fm.get_params('aperiodic_params', 'knee')
    r_sq = fm.get_params('r_squared')
 
    # saving aperiodic + periodic parameters to a list appending over all epochs
    list = (exp, offset)
    aperiodic_STN.append(list)
    
    #saving fooofed spectra for all events as a list
    list1 = (fm.fooofed_spectrum_)
    fooofed_STN.append(list1)

    #saving error
    list2 = (r_sq)
    aperiodic_STN_err.append(list2)
    


#data frame of aperiodic+periodic components
column_names_full = ["Exponent STN", "Offset STN"]
column_error = ["R_squared STN Aperiodic"]
df_aperiodic_STN = pd.DataFrame(aperiodic_STN, columns = column_names_full)       
df_aperiodic_STN_err = pd.DataFrame(aperiodic_STN_err, columns = column_error)    

#plotting fooofed spectra in one plot STN

fooofed_STN = np.asarray(fooofed_STN)
frequency = fm.freqs

beta = [df_aperiodic_STN, stn]
beta = pd.concat(beta, axis=1, join='inner')
display(beta)

# saving the dataframe 
beta.to_csv('sub006_only_beta_channel58.csv') 


lowbeta = pd.read_csv('sub006_only_low_beta_channel58.csv', index_col=[0])
beta = pd.read_csv('sub006_only_beta_channel58.csv', index_col=[0])

exp1 = lowbeta['Exponent STN']
exp2 = beta['Exponent STN']
exp = [exp1, exp2]
exponent = pd.concat(exp, axis=1, join='inner')
exponent = exponent.mean(axis = 1)

offset1 = lowbeta['Offset STN']
offset2 = beta['Offset STN']
offset = [offset1, offset2]
os = pd.concat(offset, axis=1, join='inner')
os = os.mean(axis = 1)


newlow = lowbeta.drop(['Exponent STN','Offset STN','Ampl beta STN', 'CF high beta STN', 'BW beta STN'], axis = 1)
new_beta = beta.drop(['Exponent STN','Offset STN','CF low beta STN','Ampl low beta STN','BW low beta STN'], axis=1) 
final = [exponent, os, newlow, new_beta]
df = pd.concat(final, axis=1, join='inner')

STN = df.rename(columns={0: 'Exponent STN', 1: 'Offset STN', 'CF high beta STN': 'CF beta STN'})

#FOOOF for ECoG electrode
#creating a loop over all epochs
results = []
periodic_ECoG = []
periodic_ECoG_alpha = []
periodic_ECoG_beta = []
fooofed_ECoG = []
periodic_ECoG_err = []
freq_range = [2,50]

for idx, val in enumerate(avpower_ecog[:,0]):

    #creating fooof object and performing the fitting
    fm = FOOOF(peak_width_limits=(0.05, 15.0),min_peak_height=0.05, aperiodic_mode='fixed', max_n_peaks=3)
    fm.report(freqs_wv, avpower_ecog[idx,:],freq_range,plt_log=True)  #epoch 1
#     fm.plot(plot_aperiodic=False, save_fig = True, file_name = filename + str(idx), add_legend = True) #('test.png', bbox_inches='tight')
    
    # Extract a model parameter with `get_params`
    cfs = fm.get_params('peak_params', 'CF')
    pws = fm.get_params('peak_params', 'PW')
    bws = fm.get_params('peak_params', 'BW')
    r_sq = fm.get_params('r_squared')
 
    cfs = np.array(cfs, ndmin = 1)
    pws = np.array(pws, ndmin = 1)
    bws = np.array(bws, ndmin = 1)

    # making list with alpha band peak properties
    list_alpha = []
    list_beta = []
    
    for i in range(len(cfs)):
        if cfs[i] > 8 and cfs[i] < 12:

            list_alpha = (cfs[i], pws[i], bws[i])
            periodic_ECoG_alpha.append(list_alpha)
            
            
        if cfs[i] > 12 and cfs[i] < 35:
            list_beta = (cfs[i], pws[i], bws[i])
            periodic_ECoG_beta.append(list_beta)
    
        list = (list_alpha, list_beta)
    results.append(list)

            
    #saving fooofed spectra for all events as a list
    list1 = (fm.fooofed_spectrum_)
    fooofed_ECoG.append(list1)
    
    #saving error
    list2 = (r_sq)
    periodic_ECoG_err.append(list2)


results = np.asarray(results)

#data frame of periodic components
column_error = ["R_squared ECoG Periodic"]
column_names_full = ["Central frequency ECoG", "Peak power ECoG"]
df_periodic_ECoG = pd.DataFrame(results, columns = column_names_full)
df_periodic_ECoG_err = pd.DataFrame(periodic_ECoG_err, columns = column_error)    


#expanding multiple peaks into separate columns and renaming them
s = df_periodic_ECoG.apply(lambda x: pd.Series(x['Central frequency ECoG']),axis=1,result_type='expand')
s = df_periodic_ECoG.drop('Central frequency ECoG', axis=1).join(s)
s = s.rename(columns={0: 'CF alpha ECoG', 1: 'Ampl alpha ECoG', 2: 'BW alpha ECoG'})
pw = df_periodic_ECoG.apply(lambda x: pd.Series(x['Peak power ECoG']),axis=1,result_type='expand')
s = s.drop('Peak power ECoG', axis=1).join(pw)
s = s.rename(columns={0: 'CF beta peak ECoG', 1: 'Ampl beta peak ECoG', 2: 'BW beta peak ECoG'})
s = s.rename(columns={'CF Peak 1':'CF Peak 1 ECoG', 'CF Peak 2': 'CF Peak 2 ECoG', 'PW Peak 1':'PW Peak 1 ECoG',
                      'PW Peak 2':'PW Peak 2 ECoG', 'BW Peak 1':'BW Peak 1 ECoG','BW Peak 2':'BW Peak 2 ECoG'})


#FOOOF for ECoG electrode
#creating a loop over all epochs
aperiodic_ECoG = []
aperiodic_ECoG_err = []
fooofed_ECoG = []
freq_range = [35,70]

for idx, val in enumerate(avpower_ecog[:,0]):
    print(idx)
    #creating fooof object and performing the fitting
    fm = FOOOF(peak_width_limits=(0.5, 15.0),min_peak_height=0.1, aperiodic_mode='fixed', max_n_peaks=1)
    fm.report(freqs_wv, avpower_ecog[idx,:],freq_range,plt_log=True)  #epoch 1
#     fm.plot(plot_aperiodic=False, save_fig = True, file_name = filename + str(idx), add_legend = True) #('test.png', bbox_inches='tight')
    
    # Extract a model parameter with `get_params`
#     err = fm.get_params('error')
    exp = fm.get_params('aperiodic_params', 'exponent')
    offset = fm.get_params('aperiodic_params', 'offset')
#     knee = fm.get_params('aperiodic_params', 'knee')
    r_sq = fm.get_params('r_squared')
 
        # saving aperiodic + periodic parameters to a list appending over all epochs
    list = (exp, offset)
    aperiodic_ECoG.append(list)
    
    
    #saving fooofed spectra for all events as a list
    list1 = (fm.fooofed_spectrum_)
    fooofed_ECoG.append(list1)

    #saving error
    list2 = (r_sq)
    aperiodic_ECoG_err.append(list2)

#data frame of periodic components
   
# full_ECoG = np.asarray(full_ECoG).astype(np.float)

#data frame of aperiodic components
column_names_full = ["Exponent ECoG", "Offset ECoG"]
column_error = ["R_squared ECoG Aperiodic"]
df_aperiodic_ECoG_err = pd.DataFrame(aperiodic_ECoG_err, columns = column_error)    
df_aperiodic_ECoG = pd.DataFrame(aperiodic_ECoG, columns = column_names_full)


#calculating mean error from various fooof calculations

error_full = [df_aperiodic_STN_err, df_periodic_STN_err, df_aperiodic_ECoG_err, df_periodic_ECoG_err]
result_err = pd.concat(error_full, axis=1, join='inner')
result_err['mean error'] = result_err.mean(axis=0)
error_full = np.asarray(error_full).astype(np.float)
error_full.shape
mean = np.mean(error_full, axis = 0)
df_mean = pd.DataFrame(mean, columns = ['Mean R^2'])

# full = [df_aperiodic_STN, stn, df_aperiodic_ECoG, s, df_mean]
full = [STN, df_aperiodic_ECoG, s, df_mean]
# merging data frames and creating one ECoG df
result = pd.concat(full, axis=1, join='inner')
display(result)
# saving the dataframe 
result.to_csv('sub006_ecog_stn_peaks_separately_foofed_peaks.csv') 