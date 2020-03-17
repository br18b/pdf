# pdf
Reads an input text file and creates probability distribution functions for all requested fields

The input file provides the following parameters:

-p /path/to/the/simulation

-f DD DD

the simulation files come with a certain format,
so the actual data is loaded from:
/path/to/the/simulation/DDXXXX/DDXXXX
where XXXX is a four-digit frame number.
If folders have different names, e.g. DDXXXX/dataXXXX, -f
takes care of that

-r 1 100 5

The range from which frames should be loaded, including.
Third number denotes skipping, optional. In this case, loaded frames will be:
DD0001/DD0001
DD0006/DD0006
etc.

-t	vx
	vy
	vz
	...

What fields to take distributions of. -t doesn't need to be repeated

vx lin 0.1

two optional parameters, first denotes the scale (lin for linear,
log for logarithmic, symlog for symmetric log, the number denotes in case of linear the step size,
in case of log scale nothing and in case of symlog the threshold). Default is lin with step 0.01
