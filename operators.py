import yt
import numpy

def d(data, field, dir):
	sliceR = slice(2,None)
	sliceL = slice(None,-2)
	all = slice(1,-1)
	all_all = tuple([all]*3)
	print(data)
	dxi = 1./(2*data.ds.dds)
	out = numpy.zeros_like(data[field]*dxi[0])
	left = [all]*3
	right = [all]*3
	left[dir] = sliceL
	right[dir] = sliceR
	left = tuple(left)
	right = tuple(right)
	out[all_all] = (data[field][right] - data[field][left])*dxi[dir]
	return out

def vecdotdelscalar(data, vecfield, scalfield):
	sliceR = slice(2,None)
	sliceL = slice(None,-2)
	all = slice(1,-1)
	all_all = tuple([all]*3)
	dxi = 1./(2*data.ds.dds)
	out = numpy.zeros_like(data[scalfield]*data[vecfield[0]]*dxi[0])
	temp = numpy.zeros_like(data[scalfield])
	for i, fi in enumerate(vecfield):
		left = [all]*3
		right = [all]*3
		right[i] = sliceR
		left[i] = sliceL
		left = tuple(left)
		right=tuple(light)
		all_all=tuple(all_all)
		temp[all_all] = data[scalfield][right] - data[scalfield][left]
		out[all_all] += data[fi][all_all]*(temp[all_all])*dxi[i]
	return out

#def vecdotdelvec(data, vecfield1, vecfield2):
#	
