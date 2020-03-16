fields = {"vx", "vy", "vz", "rho", "Density", "density", "drhodx", "drhody", "drhodz",
"|gradrho|", "vdotgradrho", "vdotgradrhoangle"}

def load_params(input_filename):
	input = open("input.txt", "r")
	lines = input.readlines()
	path = "~/"
	filenames = ["DD","DD"]
	frames = range(0,100)
	tasks = []
	scales = []
	for line in lines:
		tokens = line.split()
		token0 = tokens[0]
		if token0 in fields:
			token0 = "-t"
			print("!!!")
		else:
			token0 = tokens[0]
			tokens = tokens[1:]
		if token0 == "path" or token0 == "-p":
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
		elif token0 == "tasks" or token0 == "-t":
			tasks.append(tokens[0])
			if len(tokens) > 1:
				scales.append(tokens[1])
			else:
				scales.append("lin")
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
	return path, filenames, frames, tasks, scales
