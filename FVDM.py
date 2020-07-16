from pydub import AudioSegment
from detrending import normalize_amplitude, mc_detrend, ac_detrend
from statsmodels.tsa.stattools import adfuller, kpss
import matplotlib.pyplot as plt 
from nolds import hurst_rs

def FVDM(audio_path,vowel_timing=None,mcv_window_size=25,mcv_window_shift=10,
         sample_rate=44100,pvalue_cutoff=0.05,plot_components=False): 
    """
    This function calculates Filtered Vowel Distortion Measures (FVDM). 
    Returns: 
        FVDM-VS: the stability of the stationary vowel
            (if the filtered vowel is not stationary, will return None)
        FVDM-ACV: the variance of the additive component, 
            separated using empirical mode decomposition (EMD)
        FVDM-MCV: the variance of the multiplicative component, 
            separated using a windowing approach 
    Arguments: 
        audio_path: path to the wav file which contains the vowel audio 
        vowel_timing: tuple in the form of (start, end), which specifies
            the start and end times (in ms) of the vowel in the audio file 
            if none, assume the audio file is just a vowel 
        mcv_window_size: size of the window (in ms) to use for removing mc 
        mcv_window_shift: shift of the window (in ms) to use for removing mc 
        sample_rate: sample_rate of data (used in ac_detrend)
        pvalue_cutoff: p-value for assessing stationarity with Dickey-Fuller
            and KPSS tests 
        plt_components: for debugging, if True, will plot the detrending process
    """
    
    # read in audio and set to single channel 
    audio = AudioSegment.from_wav(audio_path)
    audio = audio.set_channels(1)
    
    # if audio is not just a vowel utterance, segment the vowel portion
    if isinstance(vowel_timing,tuple): 
        vowel_start = vowel_timing[0]
        vowel_end = vowel_timing[1]
        audio = audio[vowel_start:vowel_end]
                
    # check stationarity test p-values before detrending            
    audio_samples = list(audio.get_array_of_samples())            
    audio_samples = normalize_amplitude(audio_samples) 
    if plot_components: 
        plt.plot(audio_samples)
        plt.show() 
    adftest_before = adfuller(audio_samples)[1]
    kpss_before = kpss(audio_samples,nlags='legacy')[1]
      
    # remove multiplicative trend component 
    detrended, mc, mcv = mc_detrend(audio, mcv_window_size, mcv_window_shift)
    if plot_components: 
        plt.plot(detrended)
        plt.show() 
        plt.plot(mc)
        plt.show() 
    
    # remove additive trend component 
    detrended, ac, acv = ac_detrend(detrended, sample_rate) 
    if plot_components: 
        plt.plot(detrended)
        plt.show() 
        plt.plot(ac)
        plt.show() 

    # adjusting back to amplitude of [-1,1] 
    # to ensure that amplitude does not make a difference 
    # (this shouldn't actually impact HE at all and could likely be removed)
    detrended = normalize_amplitude(list(detrended)) 
            
    # check stationarity test p-values after detrending            
    adftest_after = adfuller(detrended)[1]
    kpss_after = kpss(detrended,nlags='legacy')[1]
    if adftest_after > pvalue_cutoff: 
        return None, acv, mcv
    # note the KPSS tests the opposite null hypothesis
    # i.e., LOW pvalue indicates evidence of non-stationarity
    if kpss_after < pvalue_cutoff: 
        return None, acv, mcv 

    # there is some randomness in calculating the HE 
    # calculate it 10 times and then take the median value
    vs_vals = [] 
    for i in range(10): 
         vs_vals.append(hurst_rs(detrended))
    vs = np.median(vs_vals) 

    return vs, acv, mcv
