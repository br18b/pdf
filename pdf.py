#! /usr/bin/env python
import yt, numpy, os
import load_operators
from load import load_params
from yt.funcs import mylog
import sys

mylog.setLevel(50)

def bin_size(bins):
	return bins[1:]-bins[:-1]

def bin_center(bins):
	return 0.5*(bins[1:]+bins[:-1])

input_filename = sys.argv[-1]

if(input_filename[-3:] == ".py"):
	input_filename = "input.txt"

print("loading from %s"%input_filename)

path, filenames, frames, tasks, scales, verbose = load_params(input_filename)

if not os.path.exists('%s/pdf'%path):
	os.makedirs('%s/pdf'%path)

for frame in frames:
	print("loading %s/%s%04d/%s%04d ..."%(path,filenames[0],frame,filenames[1],frame))
	ds = yt.load('%s/%s%04d/%s%04d'%(path,filenames[0],frame,filenames[1],frame))
	load_operators.reset_fields(verbose)
	load_operators.load(ds, tasks, verbose)
	region = ds.all_data()
	for i in range(len(tasks)):
		task = tasks[i]
		field_name = task
		scale_desc = scales[i]
		if scale_desc[0] == "proj" or scale_desc[0] == "projection":
			proj = yt.ProjectionPlot(ds, axis, field_name)
			if (min != "auto"):
				if verbose:
					print("creating projection of %s along %s-axis, in limits (%f, %f)"%(field_name, axis, min, max))
				proj.set_zlim(field_name, min, max)
			elif verbose:
				print("creating projection of %s along %s-axis, in automatically set limits"%(field_name, axis))
			proj.save('%s/pdf/%04d'%(path, frame))
		else:
			print("fetching data for %s"%field_name)
			data = ds.all_data()[field_name].v
			volumes = ds.all_data()['cell_volume'].v
			merged = list(zip(data,volumes))
			print("sorting... (length = %d)"%(len(data)))
			merged.sort(key=lambda x: x[0])
			print("converting back to lists...")
#			data, volumes = (list (e) for e in merged)
			data, volumes = map(list, zip(*merged))
			print("sorted!")
			n = 1000;
			V = 1.0;
			v = 0;
			e0 = data[0]
			P = []
			for i in range(len(data)):
				if (v > V/n):
					P.append([0.5*(data[i] + e0), v/(data[i] - e0)])
					v = 0
					e0 = data[i]
				v += volumes[i]
			P.append([0.5*(data[-1] + e0), v/(data[-1] - e0)])
			print('saving pdf to %s/pdf/%04d_%s.txt'%(path, frame, field_name))
			numpy.savetxt('%s/pdf/%04d_%s.txt'%(path, frame, field_name), P)
'''
		field_bins = numpy.zeros_like([])
		make_projection = False
		for j in range(len(scale_desc)):
			scale = scale_desc[j][0]

			if scale == "proj" or scale == "projection":
				make_projection = True
				axis = scale_desc[j][1]
				min = scale_desc[j][2]
				max = scale_desc[j][3]
				break

			scale_min = scale_desc[j][1]
			scale_max = scale_desc[j][2]
			N = int(scale_desc[j][3])

			if scale_min == "auto":
				minval = region[field_name].min().v
			elif scale_min == "mid":
				minval = 0.5*(region[field_name].min().v + region[field_name].max().v)
			else:
				minval = float(scale_min)
			if scale_max == "auto":
				maxval = region[field_name].max().v
			elif scale_max == "mid":
				maxval = 0.5*(region[field_name].min().v + region[field_name].max().v)
			else:
				maxval = float(scale_max)
			if verbose:
				print("scale:", scale, minval, maxval, N)
			if scale == "lin":
				if minval < 0:
					field_bins = numpy.concatenate((field_bins, numpy.linspace(minval, maxval, N)))
				else:
					field_bins = numpy.concatenate((field_bins, numpy.linspace(minval, maxval, N)))
			elif scale == "log" or scale == "logR" or scale == "logr":
				foo = 0.5*(maxval-minval+numpy.sqrt(4+(maxval - minval)**2))
				field_bins = numpy.concatenate((field_bins, numpy.full(N, minval - 1.0/foo) + numpy.logspace(numpy.log10(1.0/foo), numpy.log10(foo), N)))
			elif scale == "logL" or scale == "logl":
				foo = 0.5*(maxval-minval+numpy.sqrt(4+(maxval - minval)**2))
				field_bins = numpy.concatenate((field_bins, (numpy.full(N, maxval + 1.0/foo) - numpy.logspace(numpy.log10(1.0/foo), numpy.log10(foo), N))[::-1]))
		if make_projection:
			proj = yt.ProjectionPlot(ds, axis, field_name)
			if (min != "auto"):
				if verbose:
					print("creating projection of %s along %s-axis, in limits (%f, %f)"%(field_name, axis, min, max))
				proj.set_zlim(field_name, min, max)
			elif verbose:
				print("creating projection of %s along %s-axis, in automatically set limits"%(field_name, axis))
			proj.save('%s/pdf/%04d'%(path, frame))
		else:
			field_bins = numpy.unique(field_bins)
			if verbose:
				print("field: %s, min: %f, max: %f, number of points: %d"%(field_name, field_bins[0], field_bins[-1], field_bins.size))
			bins = {field_name: field_bins}
			profile = yt.create_profile(region, bin_fields = [field_name], fields = ['cell_volume'], weight_field = None, fractional = True, override_bins = bins)
			P = numpy.column_stack((bin_center(field_bins),profile['cell_volume']/bin_size(field_bins)))
			#numpy.savetxt('%s/pdf/%04d_%s_bad_norm.txt'%(path, frame, field_name), P)
			P = P[~numpy.isnan(P[:,1])]
			norm = sum(0.5*(P[i + 1][1] + P[i][1])*(P[i + 1][0] - P[i][0]) for i in range(len(P) - 1))
			if verbose:
				print("correcting norm: %f"%norm)
			P = [[P[i][0], P[i][1]/norm] for i in range(len(P)) if P[i][1] > 1e-10 or (i == 0 or i == len(P) - 1)]
'''
#			print('saving pdf to %s/pdf/%04d_%s.txt'%(path, frame, field_name))
#			numpy.savetxt('%s/pdf/%04d_%s.txt'%(path, frame, field_name), P)
