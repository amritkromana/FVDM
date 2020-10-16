from pydub import AudioSegment
from FVDM.detrending import normalize_amplitude, mc_detrend, ac_detrend
from statsmodels.tsa.stattools import adfuller, kpss
import matplotlib.pyplot as plt 
import nolds
from scipy.stats import linregress

def FVDM(audio_path,vowel_timing=None,mult_trend_window_size=25,
        mult_trend_window_shift=10,sample_rate=44100,plot_components=False): 
    """
    This function calculates measures of vowel changes 
    which we refer to as Filtered Vowel Distortion Measures (FVDM). 
    Returns: 
        Hurst exponent of the first IMF: quantifies the stability vs 
            roughness of the detrended noise-like component of a vowel 
            ranges from 0 to 1 
            values closer to 1 = more stable 
            values closer to 0 = more rough 
        Standard deviation of the additive trend: potentially captures 
            coarticulation impacts on vowels
        Standard deviation of the multiplicative trend: captures changes
            in volume within vowels using a windowing approach 
    Arguments: 
        audio_path: path to the wav file which contains the vowel audio 
        vowel_timing: tuple in the form of (start, end), which specifies
            the start and end times (in ms) of the vowel in the audio file 
            if none, assume the audio file is just a vowel 
        mult_trend_window_size: size of the window (in ms) to use for 
            removing mc 
        mult_trend_window_shift: shift of the window (in ms) to use for 
            removing mc 
        sample_rate: sample_rate of data (used in ac_detrend)
        plt_components: for debugging, if True, will plot the detrending 
            process
    """
    
    # read in audio and set to single channel 
    audio = AudioSegment.from_wav(audio_path)
    audio = audio.set_channels(1)
    
    # if audio is NOT just a vowel utterance, segment the vowel portion
    if isinstance(vowel_timing,tuple): 
        vowel_start = vowel_timing[0]
        vowel_end = vowel_timing[1]
        audio = audio[vowel_start:vowel_end]
      
    # remove multiplicative trend component 
    detrended, mc, std_of_mult_trend = mc_detrend(audio, mult_trend_window_size, mult_trend_window_shift)
    if plot_components: 
        plt.plot(detrended)
        plt.show() 
        plt.plot(mc)
        plt.show() 
    
    # remove additive trend component 
    detrended, pc, ac, std_of_add_trend = ac_detrend(detrended, sample_rate) 
    if plot_components: 
        plt.plot(detrended)
        plt.show() 
        plt.plot(pc)
        plt.show()
        plt.plot(ac)
        plt.show() 

    # calculate hurst exponent of the first IMF 
    # use DFA method with order = 0 
    # fit exponent using poly instead of RANSAC, based on previous work 
    # window sizes set to capture fluctuations within 2 ms to 10 ms windows
    hurst_exp_first_imf, debug_data = nolds.dfa(detrended, 
            nvals=nolds.logarithmic_n(88,441,1.05), 
            order=0, fit_exp='poly', debug_data=True) 
    
    # if R2 calculated from the log-log plot is less than 0.99, 
    # don't use hurst exponent that was calculated 
    # hurst exponent is only valid if the log-log plot has linear 
    # behavior and the line fit to the plot is a good fit 
    _, _, r_value, _, _ = linregress(debug_data[0], debug_data[1]) 
    r2 = r_value**2
    if r2 < 0.99: 
        hurst_exp_first_imf = None 

    return hurst_exp_first_imf, std_of_add_trend, std_of_mult_trend
