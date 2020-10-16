import numpy as np 
from PyEMD import EMD 


def normalize_amplitude(s):
    
    # apply a linear transformation so a series spans [-1,1]
    min_val = min(s) 
    max_val = max(s)     
    s = [2*((a-min_val)/(max_val-min_val))-1 for a in s]
    
    return s

def mc_detrend(audio,window_len=25,window_shift=10): 
    
    # initialize lists to hold detrended series and 
    # the multiplicative component (the trend that is removed)
    detrended = [] 
    mc = []

    # get target average dBFS for which to match in each window 
    target = audio.dBFS
    
    # initialize window position 
    window_start = 0
    window_end = window_start + window_len

    # loop through until the end of the window is outside of the audio
    while True: 
        
        # save the average dBFS in each window 
        mc.append(audio[window_start:window_end].dBFS)
        
        # apply the necessary gain/decay and append adjusted series to detrended
        if len(detrended) == 0: 
            detrended += audio[window_start:window_end].apply_gain(target-audio[window_start:window_end].dBFS).get_array_of_samples()
        else: 
            detrended += audio[window_start:window_end].apply_gain(target-audio[window_start:window_end].dBFS)[-window_shift:].get_array_of_samples()         

        # increment window position 
        window_start += window_shift
        window_end = window_start + window_len

        # check if window end is outside of audio 
        if window_end > len(audio): 
            break 
        
    # get standard deviation of the multiplicative component 
    std_of_mult_trend = np.std(mc)
    
    return detrended, mc, std_of_mult_trend


def ac_detrend(s,sample_rate=44100): 
    
    # s should be an array for PyEMD 
    # normalizing amplitude here so that amplitude doesn't factor 
    # in to the std of the additive trend 
    s = np.array(normalize_amplitude(s))
    
    # set up index and adjust lengths so they align 
    t = np.arange(0,len(s)/sample_rate*1000,1/(sample_rate/1000))
    if len(t) > len(s): 
        t = t[:len(s)]
    if len(s) > len(t): 
        s = s[:len(t)]

    # get IMFs using PyEMD 
    emd = EMD()
    imfs = emd(s,t)

    # first IMF is the detrended noise-like component 
    # IMFs 1 to 4 are the periodic component - currently not extracting
    # features from this component 
    # IMFs 5 and higher are the additive trend 
    detrended = imfs[0]
    pc = np.sum(imfs[1:5],axis=0)
    ac = np.sum(imfs[5:],axis=0)

    # get standard deviation of additice component
    std_of_add_trend = np.std(ac)
    
    return detrended, pc, ac, std_of_add_trend


 
