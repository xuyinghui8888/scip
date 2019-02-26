from pyscipopt import Model, quicksum, multidict



def transp(I, J, c, d, M):
	"""transp -- model for solving the transportation problem
	Parameters: 
		I - set of customers
		J - set of facilities
		c[i,j] - unit transportation cost on arc (i,j)
		d[i] - demand at node i
		M[j] - capacity
	returns a model, ready to be solved
	"""

	model=Model("transportation") 
	
	# create variables
	x={}
	for i in I:
		for j in J:
			x[i,j]=model.addVar(vtype="C",name="x(%s,%s)" % (i,j) )

	# demand constraints
	for i in I:
		model.addCons(quicksum(x[i,j] for j in J if (i,j) in x) == d[i], name="Demand(%s)" % i)

	# capacity constraints
	for j in J:
		model.addCons(quicksum(x[i,j] for i in I if (i,j) in x) <= M[j], name="Capacity(%s)" % j)

	# objective
	model.setObjective( quicksum( c[i,j]*x[i,j] for (i,j) in x), "minimize") 
	
	model.optimize()

	model.data=x

	return model

def make_inst1():
	I,d=multidict({1:80,2:270,3:250,4:160,5:100}) 	# demand
	J,M=multidict({1:500,2:500,3:500}) 				# capacity
	c={
		(1,1):4,    (1,2):6,    (1,3):9,  # const
     	(2,1):5,    (2,2):4,    (2,3):7,
     	(3,1):6,    (3,2):3,    (3,3):3,
     	(4,1):8,    (4,2):5,    (4,3):3,
     	(5,1):10,   (5,2):8,    (5,3):4,
     	}
	return I,J,c,d,M

def make_inst2():
    I,d = multidict({1:45, 2:20, 3:30 , 4:30}) # demand
    J,M = multidict({1:35, 2:50, 3:40})        # capacity
    c = {(1,1):8,    (1,2):9,    (1,3):14  ,   # {(customer,factory) : cost<float>}
         (2,1):6,    (2,2):12,   (2,3):9   ,
         (3,1):10,   (3,2):13,   (3,3):16  ,
         (4,1):9,    (4,2):7,    (4,3):5   ,
         }
    return I,J,c,d,M


if __name__=="__main__":
	I,J,c,d,M=make_inst1()
	model=transp(I,J,c,d,M)
	print("Optimal value:", model.getObjVal())
	EPS = 1.e-6
	x=model.data

	for (i,j) in x:
		if model.getVal(x[i,j])>EPS:
			print("sending quantity %10s from factory %3s to customer %3s" % (model.getVal(x[i,j]),j,i))

