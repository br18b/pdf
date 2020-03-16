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

def dvydx(field, data):
	return operators.d(data, 'z-velocity', 0)
def dvydy(field, data):
	return operators.d(data, 'z-velocity', 1)
def dvydz(field, data):
	return operators.d(data, 'z-velocity', 2)

def absgradrho(field, data):
	return (data['drhodx']**2 + data['drhody']**2 + data['drhodz']**2)**0.5

def vdotgradrho(field, data):
	return data['x-velocity']*data['drhodx'] + data['y-velocity']*data['drhody'] + data['z-velocity']*data['drhodz']

density_validators = [yt.ValidateSpatial(1,['density'])]

vx_validators = [yt.ValidateSpatial(1,['x-velocity'])]
vy_validators = [yt.ValidateSpatial(1,['y-velocity'])]
vz_validators = [yt.ValidateSpatial(1,['z-velocity'])]

density_dx_requirement_set = {"drhodx", "|gradrho|", "vdotgradrho", "vdotgradrhoangle"}
density_dy_requirement_set = {"drhody", "|gradrho|", "vdotgradrho", "vdotgradrhoangle"}
density_dz_requirement_set = {"drhodz", "|gradrho|", "vdotgradrho", "vdotgradrhoangle"}

dvxdx_requirement_set = {"dvxdx", "vdotgradv", "divv"}
dvxdy_requirement_set = {"dvxdy", "vdotgradv"}
dvxdz_requirement_set = {"dvxdz", "vdotgradv"}

dvydx_requirement_set = {"dvydx", "vdotgradv"}
dvydy_requirement_set = {"dvydy", "vdotgradv", "divv"}
dvydz_requirement_set = {"dvydz", "vdotgradv"}

dvzdx_requirement_set = {"dvzdx", "vdotgradv"}
dvzdy_requirement_set = {"dvzdy", "vdotgradv"}
dvzdz_requirement_set = {"dvzdz", "vdotgradv", "divv"}

drho_units = "code_mass/code_length**4"

dv_units = "1/code_time"

taskdictfun = {"|gradrho|": absgradrho, "absgradrho": absgradrho, "vdotgradrho": vdotgradrho}
taskdictstr = {"vx": "x-velocity", "vy": "y-velocity", "vz": "z-velocity",
"drhodx": "drhodx", "drhody": "drhody","drhodz": "drhodz",
"|gradrho|": "absgradrho", "vdotgradrho": "vdotgradrho"}
taskdictuni = {"|gradrho|": "code_mass/code_length**4", "vdotgradrho": "code_mass/(code_length**3*code_time)"}
taskdictval = {"|gradrho|": [yt.ValidateGridType()], "vdotgradrho": [yt.ValidateGridType()]}


def load(ds, tasks):
	needs_densitydx = False
	needs_densitydy = False
	needs_densitydz = False

	needs_dBxdx = False; needs_dBxdy = False; needs_dBxdz = False;
	needs_dBydx = False; needs_dBydy = False; needs_dBydz = False;
	needs_dBzdx = False; needs_dBzdy = False; needs_dBzdz = False;

	needs_dvxdx = False; needs_dvxdy = False; needs_dvxdz = False;
	needs_dvydx = False; needs_dvydy = False; needs_dvydz = False;
	needs_dvzdx = False; needs_dvzdy = False; needs_dvzdz = False;

	for task in tasks:
		field_name = taskdictstr[task]
		if needs_densitydx == False and task in density_dx_requirement_set:
			ds.add_field("drhodx", drhodx, take_log = False, validators = density_validators, sampling_type = 'cell', units = drho_units)
			print("field %s needs also field drho/dx, adding ..."%field_name)
		if needs_densitydy == False and task in density_dy_requirement_set:
			ds.add_field("drhody", drhodx, take_log = False, validators = density_validators, sampling_type = 'cell', units = drho_units)
			print("field %s needs also field drho/dy, adding ..."%field_name)
		if needs_densitydz == False and task in density_dy_requirement_set:
			ds.add_field("drhodz", drhodx, take_log = False, validators = density_validators, sampling_type = 'cell', units = drho_units)
			print("field %s needs also field drho/dz, adding ..."%field_name)

		if needs_dvxdx == False and task in dvxdx_requirement_set:
			ds.add_field("dvxdx", dvxdx, take_log = False, validators = vx_validators, sampling_type = 'cell', units = dv_units)
			print("field %s needs also field dvx/dx, adding ..."%field_name)
		if needs_dvxdy == False and task in dvxdy_requirement_set:
			ds.add_field("dvxdy", dvxdy, take_log = False, validators = vx_validators, sampling_type = 'cell', units = dv_units)
			print("field %s needs also field dvx/dy, adding ..."%field_name)
		if needs_dvxdz == False and task in dvxdz_requirement_set:
			ds.add_field("dvxdz", dvxdz, take_log = False, validators = vx_validators, sampling_type = 'cell', units = dv_units)
			print("field %s needs also field dvx/dz, adding ..."%field_name)

		if needs_dvydx == False and task in dvydx_requirement_set:
			ds.add_field("dvydx", dvydx, take_log = False, validators = vy_validators, sampling_type = 'cell', units = dv_units)
			print("field %s needs also field dvy/dx, adding ..."%field_name)
		if needs_dvydy == False and task in dvydy_requirement_set:
			ds.add_field("dvydy", dvydy, take_log = False, validators = vy_validators, sampling_type = 'cell', units = dv_units)
			print("field %s needs also field dvy/dy, adding ..."%field_name)
		if needs_dvydz == False and task in dvydz_requirement_set:
			ds.add_field("dvydz", dvydz, take_log = False, validators = vy_validators, sampling_type = 'cell', units = dv_units)
			print("field %s needs also field dvy/dz, adding ..."%field_name)

		if needs_dvzdx == False and task in dvzdx_requirement_set:
			ds.add_field("dvzdx", dvzdx, take_log = False, validators = vz_validators, sampling_type = 'cell', units = dv_units)
			print("field %s needs also field dvz/dx, adding ..."%field_name)
		if needs_dvzdy == False and task in dvzdy_requirement_set:
			ds.add_field("dvzdy", dvzdy, take_log = False, validators = vz_validators, sampling_type = 'cell', units = dv_units)
			print("field %s needs also field dvz/dy, adding ..."%field_name)
		if needs_dvzdz == False and task in dvzdz_requirement_set:
			ds.add_field("dvzdz", dvzdz, take_log = False, validators = vz_validators, sampling_type = 'cell', units = dv_units)
			print("field %s needs also field dvz/dz, adding ..."%field_name)

		if task in taskdictfun:
			field_function = taskdictfun[task]; field_units = taskdictuni[task]; field_validators = taskdictval[task]
			print("adding field %s, units: %s"%(field_name, field_units))
			ds.add_field(field_name, field_function, take_log = False, validators = field_validators, sampling_type = 'cell', units=field_units)
		else:
			print("field %s exists"%field_name)
