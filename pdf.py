import yt, numpy, os
import load_operators
from load import load_params

def bin_size(bins):
	return bins[1:]-bins[:-1]

def bin_center(bins):
	return 0.5*(bins[1:]+bins[:-1])

path, filenames, frames, tasks, scales = load_params("input.txt")

if not os.path.exists('%s/pdf'%path):
	os.makedirs('%s/pdf'%path)

taskdictstr = {"vx": "x-velocity", "vy": "y-velocity", "vz": "z-velocity",
"drhodx": "drhodx", "drhody": "drhody","drhodz": "drhodz",
"|gradrho|": "absgradrho", "vdotgradrho": "vdotgradrho"}

for frame in frames:
	print("loading %s/%s%04d/%s%04d ..."%(path,filenames[0],frame,filenames[1],frame))
	ds = yt.load('%s/%s%04d/%s%04d'%(path,filenames[0],frame,filenames[1],frame))
	load_operators.load(ds, tasks)
	region = ds.all_data()
	for i in range(len(tasks)):
		task = tasks[i]
		scale = scales[i]
		field_name = taskdictstr[task]

		minval = region[field_name].min().v
		maxval = region[field_name].max().v
		print("field: %s, min: %f, max: %f"%(field_name, minval, maxval))
		if scale == "lin":
			N = max(int((maxval-minval)/0.1), 1)
			field_bins = numpy.linspace(minval, maxval, N)
		elif scale == "log":
			N = 1000
			field_bins = numpy.logspace(numpy.log10(0.8*minval), numpy.log10(1.2*maxval), N)
		bins = {field_name: field_bins}
		profile = yt.create_profile(region, bin_fields = [field_name], fields = ['cell_volume'], weight_field = None, fractional = True, override_bins = bins)
		P = numpy.column_stack((bin_center(field_bins),profile['cell_volume']/bin_size(field_bins)))
		print('saving pdf to %s/pdf/%04d_%s.txt'%(path, frame, field_name))
		numpy.savetxt('%s/pdf/%04d_%s.txt'%(path, frame, field_name), P)
