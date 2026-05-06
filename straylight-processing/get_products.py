from nustar_gen import wrappers, info, utils
import os

obsidnum = input('ObsID: ')
regfilename = input('Region file name: ' )
module = input('FPM: ')
lc_bin_s = float(input('Light curve bin length: '))

#top = some path to your top level data directory.
here = os.getcwd()+'/'
obs = info.Observation(seqid=obsidnum, path=here, evdir=f'./{obsidnum}/event_cl', out_path=f'./{obsidnum}/event_cl/')

# Go make the region file using ds9.
# Below spawns another XSELECT run behind the scenes to apply the region filtering in DET1 coordinates

reg_file = obs.path+'/'+obs.seqid+'/event_cl/'+regfilename
filt_file = wrappers.extract_det1_events(obs.evtfiles[module][0], regfile=reg_file, elow=3, ehigh=160)
print(filt_file)
# filt_file is now the full path to the extracted event file. This is located in obs.evdir by default.

## cell 5 from guide
from astropy import units as u
time_bin = lc_bin_s*u.s
lc_script = wrappers.make_det1_lightcurve(filt_file, mod=module, elow=3, ehigh=20, time_bin=time_bin, obs=obs)
# lc_script is now the path to the nuproducts script to produce a lightcurve, which is stored in obs.out_path.
#
# Go run this in the shell
print(lc_script)

## cell 6 from guide
det1spec_script = wrappers.make_det1_spectra(filt_file, module, obs=obs)
# lc_script is now the path to the nuproducts script to produce a spectrum, which is stored in obs.out_path.
#
# Go run ths in the shell
print(det1spec_script)

## cell 7 from guide
expo_script = wrappers.make_exposure_map(obs, module, det_expo=True)

# expo_script is now the path to the nuexpomap script, which is stored in obs.out_path.
#
# If det_expo=False then this produces a Sky exposure map rather than the DET1 exposure map.
#
# Go run this in the shell
print(expo_script)
