# FVDM

The provided FVDM function calculates Filtered Vowel Distortion Measures. 
The speech used in our analysis were recordings of the Grandfather Passage (recorded at 44.1kHz). We manually segmented vowels from these speech samples, extracted FVDM, and aggregated them for each participant with the following statistics: min, median, max, range, std, mean. In our samples we found that this method effectively removed trends from read speech and quantified these trends/stability of the remaining vowels. These FVDM, coupled with existing features related to disordered speech, were able to classify premanifest vs manifest Huntington Disease with 80% accuracy (up from 63% using just the previously existing features).   

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
            the start and end times (in ms) of the vowel in the audio file. 
            if none, assume the audio file is just a vowel. 
            default is None.  
  mcv_window_size: size of the window (in ms) to use for removing mc.
            default is 25ms.  
  mcv_window_shift: shift of the window (in ms) to use for removing mc 
            default is 10ms.  
  sample_rate: sample_rate of data (used in ac_detrend)
            default is 44100.  
  pvalue_cutoff: p-value for assessing stationarity with Dickey-Fuller
            and KPSS tests 
            default is 0.05.  
  plt_components: for debugging, if True, will plot the detrending process
            default is False.  
