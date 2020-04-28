import operators, yt, numpy

def drhodx(field, data):
	return operators.d(data, 'Density', 0)
def drhody(field, data):
	return operators.d(data, 'Density', 1)
def drhodz(field, data):
	return operators.d(data, 'Density', 2)

def dvxdx(field, data):
	return operators.d(data, 'x-velocity', 0)
def dvxdy(field, data):
        return operators.d(data, 'x-velocity', 1)
def dvxdz(field, data):
        return operators.d(data, 'x-velocity', 2)

def dvydx(field, data):
	return operators.d(data, 'y-velocity', 0)
def dvydy(field, data):
	return operators.d(data, 'y-velocity', 1)
def dvydz(field, data):
	return operators.d(data, 'y-velocity', 2)

def dvzdx(field, data):
	return operators.d(data, 'z-velocity', 0)
def dvzdy(field, data):
	return operators.d(data, 'z-velocity', 1)
def dvzdz(field, data):
	return operators.d(data, 'z-velocity', 2)

def absv(field, data):
	return (data['x-velocity']**2 + data['y-velocity']**2 + data['z-velocity']**2)**0.5

def absgradrho(field, data):
	return (data['drhodx']**2 + data['drhody']**2 + data['drhodz']**2)**0.5

def vdotgradrho(field, data):
	return data['x-velocity']*data['drhodx'] + data['y-velocity']*data['drhody'] + data['z-velocity']*data['drhodz']

def vdotgradrhocos(field, data):
	return data['vdotgradrho']/(data['absgradrho']*data['absv'])

def vdotgradrhoangle(field, data):
	out = numpy.zeros_like(data['vdotgradrhocos'])
	out[:] = numpy.arccos(data['vdotgradrhocos'])
	return out

def divv(field, data):
	return data['dvxdx'] + data['dvydy'] + data['dvzdz']

def vdotgradvx(field, data):
	return data['x-velocity']*data['dvxdx'] + data['y-velocity']*data['dvxdy'] + data['z-velocity']*data['dvxdz']

def vdotgradvy(field, data):
	return data['x-velocity']*data['dvydx'] + data['y-velocity']*data['dvydy'] + data['z-velocity']*data['dvydz']

def vdotgradvz(field, data):
	return data['x-velocity']*data['dvzdx'] + data['y-velocity']*data['dvzdy'] + data['z-velocity']*data['dvzdz']

def absvdotgradv(field, data):
	return (data['vdotgradvx']**2 + data['vdotgradvy']**2 + data['vdotgradvz']**2)**0.5

def vdotvdotgradv(field, data):
	return data['x-velocity']*data['vdotgradvx'] + data['y-velocity']*data['vdotgradvy'] + data['z-velocity']*data['vdotgradvz']

def rhodivv(field, data):
	return data['Density']*data['divv']

def vdotvdotgradvcos(field, data):
	return data['vdotvdotgradv']/(data['absv']*data['absvdotgradv'])

def vdotvdotgradvangle(field, data):
	out = numpy.zeros_like(data['vdotvdotgradvcos'])
	out[:] = numpy.arccos(data['vdotvdotgradvcos'])
	return out

def logrho(field, data):
	rho0 = data.ds.quan(1., 'code_mass/code_length**3')
	out = numpy.zeros_like(data['Density']/rho0)
	rho = data['Density']/rho0
	out[:] = numpy.log(rho[:])
	return out

def rhologrho(field, data):
	return data['Density']*data['logrho']

def cs2rhologrho(field, data):
	cs2 = data.ds.quan(1., 'code_velocity**2')
	return cs2*data['rhologrho']

def ek(field, data):
	return 0.5*data['Density']*data['absv']**2

default_validators = [yt.ValidateGridType()]
density_validators = [yt.ValidateSpatial(1,['density'])]
vx_validators = [yt.ValidateSpatial(1,['x-velocity'])]
vy_validators = [yt.ValidateSpatial(1,['y-velocity'])]
vz_validators = [yt.ValidateSpatial(1,['z-velocity'])]

drho_units = "code_mass/code_length**4"
dv_units = "1/code_time"
a_units = "code_length/code_time**2"

fields = {
"drhodx": [drhodx, density_validators, drho_units, {}],
"drhody": [drhody, density_validators, drho_units, {}],
"drhodz": [drhodz, density_validators, drho_units, {}],
"absv": [absv, "code_length/code_time", {}],
"dvxdx": [dvxdx, vx_validators, dv_units, {}],
"dvxdy": [dvxdy, vx_validators, dv_units, {}],
"dvxdz": [dvxdz, vx_validators, dv_units, {}],
"dvydx": [dvydx, vy_validators, dv_units, {}],
"dvydy": [dvydy, vy_validators, dv_units, {}],
"dvydz": [dvydz, vy_validators, dv_units, {}],
"dvzdx": [dvzdx, vz_validators, dv_units, {}],
"dvzdy": [dvzdy, vz_validators, dv_units, {}],
"dvzdz": [dvzdz, vz_validators, dv_units, {}],
"divv": [divv, dv_units, {"dvxdx", "dvydy", "dvzdz"}],
"absgradrho": [absgradrho, drho_units, {"drhodx", "drhody,", "drhodz"}],
"vdotgradrho": [vdotgradrho, "code_mass/(code_length**3*code_time)", {"drhodx", "drhody", "drhodz"}],
"vdotgradrhocos": [vdotgradrhocos, "dimensionless", {"vdotgradrho", "absv", "absgradrho"}],
"vdotgradrhoangle": [vdotgradrhoangle, "dimensionless", {"vdotgradrhocos"}],
"vdotgradvx": [vdotgradvx, a_units, {"dvxdx", "dvxdy", "dvxdz"}],
"vdotgradvy": [vdotgradvy, a_units, {"dvydx", "dvydy", "dvydz"}],
"vdotgradvz": [vdotgradvz, a_units, {"dvzdx", "dvzdy", "dvzdz"}],
"vdotvdotgradv": [vdotvdotgradv, "code_length**2/code_time**3", {"vdotgradvx", "vdotgradvy", "vdotgradvz"}],
"rhodivv": [rhodivv, "code_mass/(code_length**3*code_time)", {"divv"}],
"absvdotgradv": [absvdotgradv, a_units, {"vdotgradvx", "vdotgradvy", "vdotgradvz"}],
"vdotvdotgradvcos": [vdotvdotgradvcos, default_validators, "dimensionless", {"vdotvdotgradv", "absv", "absvdotgradv"}],
"vdotvdotgradvangle": [vdotvdotgradvangle, default_validators, "dimensionless", {"vdotvdotgradvcos"}],
"logrho": [logrho, default_validators, "dimensionless", {}],
"rhologrho": [rhologrho, default_validators, "code_mass/code_length**3", {"logrho"}],
"cs2rhologrho": [cs2rhologrho, default_validators, "code_mass/(code_length*code_time**2)", {"rhologrho"}],
"ek": [ek, default_validators, "code_mass/(code_length*code_time**2)", {"absv"}]
}

bools = [False]*len(fields)

i = 0
for task in fields:
	fields[task].append(bools[i])
	i += 1

def reset_fields(verbose):
	if verbose:
		print("resetting fields")
		i = 0
		for key in fields:
			if fields[key][-1] == True:
				fields[key][-1] = False
				print("field %s was reset"%key)
				i += 1
		print("total %d fields were reset"%i)
	else:
		for key in fields:
			fields[key][-1] = False

def add_field(ds, task, verbose):
	fun = fields[task][0]
	vals = default_validators
	units = fields[task][-3]
	if len(fields[task]) == 5:
		vals = fields[task][1]
	if verbose:
		print("add_field: adding %s"%task)
		print("\tfunction:",fun)
		print("\tvalidators:", vals)
		print("\tunits: %s"%units)
	ds.add_field(task, fun, take_log = False, validators = vals, sampling_type = 'cell', units = units)

def dependencies(task):
	if fields.get(task) == None:
		return {}
	return fields[task][-2]

def add_fields(ds, task, verbose):
	if verbose:
		print("add_fields: %s"%task)
	dep = dependencies(task)
	if dep != {}:
		if verbose:
			print("add_fields, %s has dependencies:"%task)
			print(dep)
		for field in dep:
			add_fields(ds, field, verbose)
		add_field(ds, task, verbose)
	else:
		if verbose:
			print("add_fields, %s does not have dependencies"%task)
		if fields[task][-1] == False:
			add_field(ds, task, verbose)
			fields[task][-1] = True

def load(ds, tasks, verbose):
	for task in tasks:
		if verbose:
			print("load: %s"%task)
		if fields.get(task) != None:
			if verbose:
				print("load: %s needs to be added"%task)
			dep = dependencies(task)
			if dep == {}:
				if fields[task][4] == False:
					add_field(ds, task, verbose)
			else:
				add_fields(ds, task, verbose)
		else:
			if verbose:
				print("load: %s is one of the computed fields"%task)
