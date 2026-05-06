from astropy import units as u
from astropy.time import Time
import numpy
import math

print(f'Using whatever orbital ephemeris is enabled, this script will return the start and end phase of a given observation')
print(f'It is also capable of providing the duration (in s) between the start of an observation and the next occurance of a desired phase')
print(f'Please enter OBS start and end times in UTC, ISOT format (e.g.: 2001-02-20T17:45:52)')
print(f'This information should be contained in the header of you .evt file')
got_start = False
got_end = False
got_phi = False ## This can be hardcoded to TRUE to skip determination of a particular phase

while not got_start:
  obs_start_str = input(f'Obs. start time: ')
  try:
    obs_start = Time(obs_start_str, format='isot', scale='utc')
    got_start = True
  except:
    print('Issue parsing observation start time')
    print('Please try again')

while not got_end:
  obs_start_str = input(f'Obs. end time: ')
  try:
    obs_end = Time(obs_end_str, format='isot', scale='utc')
    got_end = True
  except:
    print('Issue parsing observation end time')
    print('Please try again')

while not got_phi:
  phi_str = input(f'Request time to phase: ... (enter 'n' to skip)')
  if not phi_str in ['n', 'N', 'no', 'No', 'NO']:
    try:
      give_phase = float(phi_str)
      got_phi = True
    except:
      print('Issue parsing phase requested')
      print('Please try again')

#### Ephemerides: the following are for 4U 1700-377, 
#### but any other source's ephemeris should, I hope, but plug-and-play
#################################################################
## Orbital ephemeris from Falanga et al 2015
# orb_epoch = 48900.373 ## units MJD
# Porb_0 = 3.411581 ## unit days D
# Porb_rch = -3.3E-6 ## unit yrs^-1
# Porb_rch *= 1/365.242374 ## units D^-1
#################################################################
#################################################################
#### Do not change anything in here unless well informed
## Orbital ephemeris from Islam and Paul 2016
orb_epoch = 49149.412 ## units MJD
Porb_0 = 3.411660 ## unit days D
Porb_rch = -4.7E-7 ## unit yrs^-1
Porb_rch *= 1/365.242374 ## units D^-1
#################################################################

obs_start_MJD = obs_start.mjd
obs_end_MJD = obs_end.mjd

# print(f'Obs start date {obs_start_MJD} (MJD)')

time_since_epoch = obs_start_MJD - orb_epoch

Porb_current = Porb_0 + (time_since_epoch*Porb_rch)
# print(f'Current orbital period {Porb_current}') ## uncomment this to announce orbital period at start of obs (e.g. curious about orbital decay)

orbs_since_epoch = math.floor(time_since_epoch/Porb_current)
# print(f'orbs since epoch = {orbs_since_epoch}') ## troubleshooting statement, likely not of utility

t_last_orb = orb_epoch + Porb_current*orbs_since_epoch
## print(f'time of last eclipse = {t_last_orb}') ## uncomment this to announce the most recent eclipse prior to the start of observation

orb_phase_start = (obs_start_MJD - t_last_orb)/Porb_current
print(f'Obs. starts at orbital phase {orb_phase_start}')

orb_phase_end = (obs_end_MJD - t_last_orb)/Porb_current
print(f'Obs. ends at orbital phase {orb_phase_end}')

## if an intermediate phase was requested, test and return the time it occured at
try: 
  time_of_interest = give_phase * Porb_current + t_last_orb - obs_start_MJD
  time_of_interest *= 24*60*60
  print(f'Obs. reaches phase {give_phase} at time {time_of_interest} s from OBS start')
except:
  pass
