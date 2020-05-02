fields = {"vx": "x-velocity", "vy": "y-velocity", "vz": "z-velocity", "x-velocity": "x-velocity",
"y-velocity": "y-velocity", "z-velocity": "z-velocity",
"dvxdx": "dvxdx", "dvxdy": "dvxdy", "dvxdz": "dvxdz",
"dvydx": "dvydx", "dvydy": "dvydy", "dvydz": "dvydz",
"dvzdx": "dvzdx", "dvzdy": "dvzdy", "dvzdz": "dvzdz",
"rho": "Density", "absv": "absv",
"Density": "Density", "density": "Density", "drhodx": "drhodx", "drhody": "drhody",
"drhodz": "drhodz", "|gradrho|": "absgradrho", "absgradrho": "absgradrho", "vdotgradrho": "vdotgradrho",
"v.gradrho": "vdotgradrho", "v.gradrhoangle": "vdotgradrhoangle", "vdotgradrhocos": "vdotgradrhocos",
"v.gradrhocos": "vdotgradrhocos",
"vdotgradrhoangle": "vdotgradrhoangle", "divv": "divv", "div.v": "divv", "vdotgradvx": "vdotgradvx",
"v.gradvx": "vdotgradvx", "v.grad vx": "vdotgradvx", "vdotgradvy": "vdotgradvy",
"v.gradvy": "vdotgradvy", "v.grad vy": "vdotgradvy", "vdotgradvz": "vdotgradvz",
"v.gradvz": "vdotgradvz", "v.grad vz": "vdotgradvz", "vdotvdotgradv": "vdotvdotgradv",
"v.grad.v.grad.v": "vdotgradvdotgradv", "v.(v.gradv)": "vdotgradvdotgradv",
"rhodivv": "rhodivv", "rhodiv.v": "rhodivv", "absvdotgradv": "absvdotgradv",
 "vdotvdotgradvcos": "vdotvdotgradvcos", "|vdotgradv|": "absvdotgradv",
"|v.gradv|": "absvdotgradv", "vdotvdotgradvangle": "vdotvdotgradvangle", "rhologrho": "rhologrho",
"Ek": "ek", "ek": "ek",  "Ep": "cs2rhologrho", "ep": "cs2rhologrho"}

def load_params(input_filename):
	input = open(input_filename, "r")
	lines = input.readlines()
	path = "."
	filenames = ["DD","DD"]
	frames = range(0,100)
	tasks = []
	scales = []
	eos = "rhologrho"
	verbose = False
	for line in lines:
		tokens = line.split()
		token0 = tokens[0]
		if token0 in fields:
			token0 = "-t"
		else:
			token0 = tokens[0]
			tokens = tokens[1:]
		if token0 == "path" or token0 == "-p":
			if len(tokens) > 0:
				path = tokens[0]
				if path[-1] == "/":
					path = path[:-1]
		elif token0 == "filenames" or token0 == "-f":
			filenames[0] = tokens[0]
			filenames[1] = tokens[1]
		elif token0 == "range" or token0 == "-r":
			start = int(tokens[0])
			end = int(tokens[1])+1
			skip = 1
			if len(tokens) > 2:
				skip = int(tokens[2])
			frames = range(start, end, skip)
		elif token0 == "verbose" or token0 == "-v":
			verbose = True
		elif token0 == "tasks" or token0 == "-t":
			tasks.append(fields[tokens[0]])
			tokens = tokens[1:]
			scales.append([])
			number_of_ranges = -(-len(tokens)//4)
			print("tokens length: %d, number of ranges: %d"%(len(tokens), number_of_ranges))
			for i in range(number_of_ranges):
				if i < number_of_ranges-1:
					scales[-1].append([tokens[4*i], tokens[4*i+1], tokens[4*i+2], tokens[4*i+3]])
				else:
					if len(tokens) % 4 == 1:
						scales[-1].append([tokens[4*i+1], "auto", "auto", 1000])
					elif len(tokens) % 4 == 2:
						scales[-1].append([tokens[4*i+1], tokens[4*i+2], "auto", 1000])
					elif len(tokens) % 4 ==3:
						scales[-1].append([tokens[4*i+1], tokens[4*i+2], tokens[4*i+3], 1000])
					elif len(tokens) % 4 == 0:
						scales[-1].append([tokens[4*i], tokens[4*i+1], tokens[4*i+2], tokens[4*i+3]])
			if len(tokens) == 0:
				scales[-1].append(["lin", "auto", "auto", 1000])
		elif token0 == "-eos":
			eos = tokens[0]
		last_token = token0
	input.close()
	print("path: %s"%(path))
	print("data file names: %sXXXX/%sXXXX"%(filenames[0],filenames[1]))
	if len(frames) > 1 and frames[2]-frames[1] > 1:
	        print("frames: %s%04d/%s%04d to %s%04d/%s%04d, skip %d"%(
	filenames[0], frames[0], filenames[1], frames[0],
	filenames[0], frames[-1], filenames[1], frames[-1], frames[2]-frames[1]-1))
	else:
	        print("frames: %s%04d/%s%04d to %s%04d/%s%04d, no skipping"%(
	filenames[0], frames[0], filenames[1], frames[0],
	filenames[0], frames[-1], filenames[1], frames[-1]))
	print("tasks:\n")
	for i in range(len(tasks)):
		if scales[i] == "lin":
			print("field: %s, in linear scale"%tasks[i])
		elif scales[i] == "log":
			print("field: %s, in logarithmic scale"%tasks[i])
		elif scales[i] == "symlog":
			print("field: %s, in symmetric logarithmic scale"%tasks[i])
	return path, filenames, frames, tasks, scales, verbose
