# TPS-Landmark-distances

This program automatically calculates Euclidian distances of TPS coordinates from tps_dig landmark digitizations.
The tps-programs can be downloaded here: <http://life.bio.sunysb.edu/ee/rohlf/software.html>

1) Choose the measurements names and configurations in the format shown in "Test_metadata.txt":
for instance:

(1, 2);interorbital DIstance iO

(5, 2);PO

(3, 10);SL

2) Program usage:

$   python TPS_Landmarks_v1.py "TPS_input_name.TPS" "outfile_name.csv" "metafile_name.txt"

"TPS_input_name.TPS"... name of your TPS file

"outfile_name.csv" ... type in any name you want

"metafile_name.txt"... name of your metadata (see point 1 above).

