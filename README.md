# FVDM

The FVDM function calculates our proposed vowel measures. FVDM = Filtered Vowel Distortion Measures. 
The speech used in our analysis were recordings of the Grandfather Passage (sampled at 44.1 kHz). We manually segmented vowels from these speech samples, extracted FVDM, and aggregated them for each participant: min, median, max, range, st dev, mean. In our samples we found that this method effectively quantified the trends/stability of the vowels, and were significantly correlated with Huntington Disease manifestation.    

## Returns
  hurst_exp_first_imf: The Hurst exponent of the first intrinsic mode 
	function (IMF) after performing empirical mode decomposition (EMD). 
	This value cannot be calculated for all series, and may return None.
	Otherwise, it will range from 0 to 1 with values closer to 1 
	indicating more vowel stability or smoothness, and values closer
	to 0 indicating more roughness. 
  std_of_add_trend: The additive trend is separated using EMD,
	and this value will be the standard deviation of this trend.  
  std_of_mult_trend: The multiplicative trend is separated using a windowing
	approach, and this value is the standard deviation of that trend. 
## Arguments
  audio_path: Path to the wav file which contains the vowel audio  
  vowel_timing: Tuple in the form of (start, end), which specifies
            the start and end times (in ms) of the vowel in the audio file. 
            If none, assume the audio file is just a vowel. 
            Default is None.  
  mult_trend_window_size: Size of the window (in ms) to use for removing 
	    the multiplicative trend.
            Default is 25ms.  
  mult_trend_window_shift: Shift of the window (in ms) to use for removing 
	    the multiplicative trend.  
            Default is 10ms.  
  sample_rate: Sample_rate of data (used in ac_detrend) 
            Default is 44100.  
  plt_components: For debugging, if True, will plot the detrending process
            Default is False.  
