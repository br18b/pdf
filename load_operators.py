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

density_validators = [yt.ValidateSpatial(1,['density'])]

vx_validators = [yt.ValidateSpatial(1,['x-velocity'])]
vy_validators = [yt.ValidateSpatial(1,['y-velocity'])]
vz_validators = [yt.ValidateSpatial(1,['z-velocity'])]

drho_units = "code_mass/code_length**4"

dv_units = "1/code_time"

a_units = "code_length/code_time**2"

possible_fields = ["drhodx", "drhody", "drhodz", "absv", "dvxdx", "dvxdy", "dvxdz",
"dvydx", "dvydy", "dvydz", "dvzdx", "dvzdy", "dvzdz", "divv", "absgradrho", "vdotgradrho",
"vdotgradrhocos", "vdotgradrhoangle", "vdotgradvx", "vdotgradvy", "vdotgradvz", "vdotvdotgradv",
"rhodivv", "absvdotgradv", "vdotvdotgradvcos", "vdotvdotgradvangle"]

field_functions = [drhodx, drhody, drhodz, absv, dvxdx, dvxdy, dvxdz,
dvydx, dvydy, dvydz, dvzdx, dvzdy, dvzdz, divv, absgradrho, vdotgradrho,
vdotgradrhocos, vdotgradrhoangle, vdotgradvx, vdotgradvy, vdotgradvz,
vdotvdotgradv, rhodivv, absvdotgradv, vdotvdotgradvcos, vdotvdotgradvangle]

bools = [False]*len(possible_fields)

dependencies = {
"divv": {"dvxdx", "dvydy", "dvzdz"},
"absgradrho": {"drhodx", "drhody", "drhodz"},
"vdotgradrho": {"drhodx", "drhody", "drhodz"},
"vdotgradrhocos": {"vdotgradrho", "absv", "absgradrho"},
"vdotgradrhoangle": {"vdotgradrhocos"},
"vdotgradvx": {"dvxdx", "dvxdy", "dvxdz"},
"vdotgradvy": {"dvydx", "dvydy", "dvydz"},
"vdotgradvz": {"dvzdx", "dvzdy", "dvzdz"},
"vdotvdotgradv": {"vdotgradvx", "vdotgradvy", "vdotgradvz"},
"rhodivv": {"divv"},
"absvdotgradv": {"vdotgradvx", "vdotgradvy", "vdotgradvz"},
"vdotvdotgradvcos": {"vdotvdotgradv", "absv", "absvdotgradv"},
"vdotvdotgradvangle": {"vdotvdotgradvcos"}
}

is_added = {}
task_to_field = {}

for i in range(len(possible_fields)):
	is_added[possible_fields[i]] = bools[i]
	task_to_field[possible_fields[i]] = field_functions[i]

default_validators = [yt.ValidateGridType()]
density_validators = [yt.ValidateSpatial(1,['density'])]
vx_validators = [yt.ValidateSpatial(1,['x-velocity'])]
vy_validators = [yt.ValidateSpatial(1,['y-velocity'])]
vz_validators = [yt.ValidateSpatial(1,['z-velocity'])]

validators = {"drhodx": density_validators, "drhody": density_validators, "drhodz": density_validators,
"dvxdx": vx_validators, "dvxdy": vx_validators, "dvxdz": vx_validators,
"dvydx": vy_validators, "dvydy": vy_validators, "dvydz": vy_validators,
"dvzdx": vz_validators, "dvzdy": vz_validators, "dvzdz": vz_validators,
"divv": default_validators, "vdotgradvx": default_validators, "vdotgradvy": default_validators,
"vdotgradvz": default_validators, "vdotvdotgradv": default_validators,
"absv": default_validators, "absgradrho": default_validators, "vdotgradrho": default_validators,
"vdotgradrhocos": default_validators, "vdotgradrhoangle": default_validators, "rhodivv": default_validators,
"rhodivv": default_validators, "absvdotgradv": default_validators,
"vdotvdotgradvcos": default_validators, "vdotvdotgradvangle": default_validators}

units = {"drhodx": drho_units, "drhody": drho_units, "drhodz": drho_units,
"dvxdx": dv_units, "dvxdy": dv_units, "dvxdz": dv_units,
"dvydx": dv_units,"dvydy": dv_units,"dvydz": dv_units,
"dvzdx": dv_units,"dvzdy": dv_units,"dvzdz": dv_units,
"absv": "code_length/code_time", "divv": dv_units,
"absgradrho": drho_units, "vdotgradrho": "code_mass/(code_length**3*code_time)",
"divv": dv_units, "vdotgradvx": a_units, "vdotgradvy": a_units, "vdotgradvz": a_units,
"vdotgradrhocos": "dimensionless", "vdotgradrhoangle": "dimensionless",
"vdotvdotgradv": "code_length**2/code_time**3", "rhodivv": "code_mass/(code_length**3*code_time)",
"rhodivv": "code_mass/(code_length**3*code_time)", "absvdotgradv": a_units,
"vdotvdotgradvcos": "dimensionless", "vdotvdotgradvangle": "dimensionless"}

def add_fields(ds, task):
	if dependencies.get(task) != None:
		for field in dependencies[task]:
			add_fields(ds, field)
		ds.add_field(task, task_to_field[task], take_log = False, validators = validators[task], sampling_type = 'cell', units = units[task])
	else:
		if is_added.get(task) == False:
			ds.add_field(task, task_to_field[task], take_log = False, validators = validators[task], sampling_type = 'cell', units = units[task])

def load(ds, tasks):
	for task in tasks:
		if dependencies.get(task) == None:
			if task_to_field.get(task) != None and is_added.get(task) == False:
				ds.add_field(task, task_to_field[task], take_log = False, validators = validators[task], sampling_type = 'cell', units = units[task])
		else:
			add_fields(ds, task)
