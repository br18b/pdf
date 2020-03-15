import yt, numpy
import operators
from load import load_params

path, filenames, frames, tasks = load_params("input.txt")

def absgradrho(field, data):
	return (operators.d(data,'Density',0)**2 + operators.d(data,'Density',1)**2 + operators.d(data,'Density',2)**2)**0.5

taskdictstr = {"vx": "x-velocity", "vy": "y-velocity", "vz": "z-velocity", "|gradrho|": "absgradrho"}
taskdictfun = {"|gradrho|": absgradrho}
taskdictuni = {"|gradrho|": "code_mass/code_length**4"}

for frame in frames:
	print("loading %s/%s%04d/%s%04d ..."%(path,filenames[0],frame,filenames[1],frame))
	ds = yt.load('%s/%s%04d/%s%04d'%(path,filenames[0],frame,filenames[1],frame))
	for task in tasks:
		field_name = taskdictstr[task]
		if task in taskdictfun.keys():
			field_function = taskdictfun[task]; field_units = taskdictuni[task]
			print("adding field %s, units: %s"%(field_name, field_units))
			ds.add_field(field_name, field_function, units=field_units)
		else:
			print("field %s exists"%field_name)
		region = ds.all_data()
		minval = region[field_name].min().v
		maxval = region[field_name].max().v
		N = max(int((maxval-minval)/0.01), 1)
		print("field: %s, min: %f, max: %f"%(field_name, minval, maxval))
		field_bins = numpy.linspace(minval, maxval, N)
		bins = {field_name: field_bins}
		profile = yt.create_profile(region, bin_fields = [field_name], fields = ['cell_volume'], weight_field = None, fractional = True, override_bins = bins)
