import yt, numpy, os
import operators
from load import load_params

def bin_size(bins):
	return bins[1:]-bins[:-1]

def bin_center(bins):
	return 0.5*(bins[1:]+bins[:-1])

path, filenames, frames, tasks = load_params("input.txt")

if not os.path.exists('%s/pdf'%path):
	os.makedirs('%s/pdf'%path)

def drhodx(field, data):
	return operators.d(data, 'Density', 0)

def drhody(field, data):
	return operators.d(data, 'Density', 1)

def drhodz(field, data):
	return operators.d(data, 'Density', 2)

def absgradrho(field, data):
	return (data['drhodx']**2 + data['drhody']**2 + data['drhodz']**2)**0.5

density_validators = [yt.ValidateSpatial(1,['density'])]

taskdictstr = {"vx": "x-velocity", "vy": "y-velocity", "vz": "z-velocity", "drhodx": "drhodx", "drhody": "drhody","drhodz": "drhodz","|gradrho|": "absgradrho"}
taskdictfun = {"drhodx": drhodx, "drhody": drhody, "drhodz": drhodz, "|gradrho|": absgradrho}
taskdictuni = {"drhodx": "code_mass/code_length**4", "drhody": "code_mass/code_length**4", "drhodz": "code_mass/code_length**4", "|gradrho|": "code_mass/code_length**4"}
taskdictval = {"drhodx": density_validators, "drhody": density_validators, "drhodz": density_validators, "|gradrho|": [yt.ValidateGridType()]}

for frame in frames:
	print("loading %s/%s%04d/%s%04d ..."%(path,filenames[0],frame,filenames[1],frame))
	ds = yt.load('%s/%s%04d/%s%04d'%(path,filenames[0],frame,filenames[1],frame))
	for task in tasks:
		field_name = taskdictstr[task]
		if task in taskdictfun.keys():
			field_function = taskdictfun[task]; field_units = taskdictuni[task]; field_validators = taskdictval[task]
			print("adding field %s, units: %s"%(field_name, field_units))
			ds.add_field(field_name, field_function, take_log = False, validators = field_validators, sampling_type = 'cell', units=field_units)
		else:
			print("field %s exists"%field_name)
		region = ds.all_data()
		minval = region[field_name].min().v
		maxval = region[field_name].max().v
		N = max(int((maxval-minval)/0.1), 1)
		print("field: %s, min: %f, max: %f"%(field_name, minval, maxval))
		field_bins = numpy.linspace(minval, maxval, N)
		bins = {field_name: field_bins}
		profile = yt.create_profile(region, bin_fields = [field_name], fields = ['cell_volume'], weight_field = None, fractional = True, override_bins = bins)
		P = numpy.column_stack((bin_center(field_bins),profile['cell_volume']/bin_size(field_bins)))
		print('saving pdf to %s/pdf/%04d_%s.txt'%(path, frame, field_name))
		numpy.savetxt('%s/pdf/%04d_%s.txt'%(path, frame, field_name), P)
