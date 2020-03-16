import yt, numpy, os
import load_operators
from load import load_params
from yt.funcs import mylog
mylog.setLevel(50)

def bin_size(bins):
	return bins[1:]-bins[:-1]

def bin_center(bins):
	return 0.5*(bins[1:]+bins[:-1])

path, filenames, frames, tasks, scales, dxs = load_params("input.txt")

if not os.path.exists('%s/pdf'%path):
	os.makedirs('%s/pdf'%path)

taskdictstr = {"vx": "x-velocity", "vy": "y-velocity", "vz": "z-velocity",
"|gradrho|": "absgradrho"}

for frame in frames:
	print("loading %s/%s%04d/%s%04d ..."%(path,filenames[0],frame,filenames[1],frame))
	ds = yt.load('%s/%s%04d/%s%04d'%(path,filenames[0],frame,filenames[1],frame))
	load_operators.load(ds, tasks)
	region = ds.all_data()
	for i in range(len(tasks)):
		task = tasks[i]
		scale = scales[i]
		dx = dxs[i]
		if task in taskdictstr:
			field_name = taskdictstr[task]
		else:
			field_name = task

		minval = region[field_name].min().v
		maxval = region[field_name].max().v
		print("field: %s, min: %f, max: %f"%(field_name, minval, maxval))
		if scale == "lin":
			N = max(int((maxval-minval)/dx), 1)
			field_bins = numpy.linspace(minval, maxval, N)
		elif scale == "log":
			N = 1000
			field_bins = numpy.logspace(numpy.log10(0.8*minval), numpy.log10(1.2*maxval), N)
		elif scale == "symlog":
			N = 1000
			field_bins = numpy.logspace(-5, numpy.log10(1.2*max(abs(minval), abs(maxval))), N)
			field_bins = (-field_bins)[::-1] + field_bins
		bins = {field_name: field_bins}
		profile = yt.create_profile(region, bin_fields = [field_name], fields = ['cell_volume'], weight_field = None, fractional = True, override_bins = bins)
		P = numpy.column_stack((bin_center(field_bins),profile['cell_volume']/bin_size(field_bins)))
		norm = sum(0.5*(P[i + 1][1] + P[i][1])*(P[i + 1][0] - P[i][0]) for i in range(len(P) - 1))
		print("correcting norm: %f"%norm)
		P = [[P[i][0], P[i][1]/norm] for i in range(len(P)) if P[i][1] > 1e-10 or (i == 0 or i == len(P) - 1)]
		print('saving pdf to %s/pdf/%04d_%s.txt'%(path, frame, field_name))
		numpy.savetxt('%s/pdf/%04d_%s.txt'%(path, frame, field_name), P)
