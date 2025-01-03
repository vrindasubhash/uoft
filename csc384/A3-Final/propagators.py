############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 3 Starter Code
## v1.0
##
############################################################


def prop_FC(csp, last_assigned_var=None):
    """
    This is a propagator to perform forward checking. 

    First, collect all the relevant constraints.
    If the last assigned variable is None, then no variable has been assigned 
    and we are performing propagation before search starts.
    In this case, we will check all the constraints.
    Otherwise, we will only check constraints involving the last assigned variable.

    Among all the relevant constraints, focus on the constraints with one unassigned variable. 
    Consider every value in the unassigned variable's domain, if the value violates 
    any constraint, prune the value. 

    :param csp: The CSP problem
    :type csp: CSP
        
    :param last_assigned_var: The last variable assigned before propagation.
        None if no variable has been assigned yet (that is, we are performing 
        propagation before search starts).
    :type last_assigned_var: Variable

    :returns: The boolean indicates whether forward checking is successful.
        The boolean is False if at least one domain becomes empty after forward checking.
        The boolean is True otherwise.
        Also returns a list of variable and value pairs pruned. 
    :rtype: boolean, List[(Variable, Value)]
    """
    pruned = []  # list to track pruned (Variable, Value) pairs

    # determine which constraints to check
    relevant_constraints = (
        csp.get_all_cons() if last_assigned_var is None else csp.get_cons_with_var(last_assigned_var)
    )

    # process each relevant constraint
    for constraint in relevant_constraints:
        # skip constraints that are already assigned or have more than one unassigned variable
        if constraint.get_num_unassigned_vars() != 1:
            continue

        # get the unassigned variable in this constraint
        unassigned_var = constraint.get_unassigned_vars()[0]

        # check all the values in the unassigned variables domain
        for value in unassigned_var.cur_domain():
            # temporarily assign a value and check if it satisfies the constraint
            unassigned_var.assign(value)
            if not constraint.check([v.get_assigned_value() if v.is_assigned() else value for v in constraint.get_scope()]):
                # if value is invalid, prune it
                unassigned_var.prune_value(value)
                pruned.append((unassigned_var, value))
            unassigned_var.unassign()  # unassign after checking

        # if the domain of the unassigned variable is empty after pruning, return fail
        if unassigned_var.cur_domain_size() == 0:
            return False, pruned

    # forward checking successful
    return True, pruned


def revise(var, constraint, prunings):
    """
    Revise the domain of var to restore arc-consistency with respect to a constraint.

    :param var: The variable whose domain needs to be revised
    :type var: Variable
    :param constraint: The constraint to be considered
    :type constraint: Constraint
    :param prunings: List of variable-value pairs that have been pruned
    :type prunings: List[(Variable, Value)]

    :returns: True if any value was pruned, False otherwise
    :rtype: boolean
    """
    revised = False
    for value in var.cur_domain():
        # check if there is a satisfying assignment for the constraint with the current value
        satisfies_constraint = False
        for sat_tuple in constraint.sat_tuples:
            if sat_tuple[constraint.get_scope().index(var)] == value:
                # check if all other variables in the tuple can take values in their current domains
                if all(v == var or v.in_cur_domain(sat_tuple[i]) for i, v in enumerate(constraint.get_scope())):
                    satisfies_constraint = True
                    break

        if not satisfies_constraint:
            var.prune_value(value)
            prunings.append((var, value))
            revised = True

    return revised


def prop_AC3(csp, last_assigned_var=None):
    """
    This is a propagator to perform the AC-3 algorithm.

    Keep track of all the constraints in a queue (list). 
    If the last_assigned_var is not None, then we only need to 
    consider constraints that involve the last assigned variable.

    For each constraint, consider every variable in the constraint and 
    every value in the variable's domain.
    For each variable and value pair, prune it if it is not part of 
    a satisfying assignment for the constraint. 
    Finally, if we have pruned any value for a variable,
    add other constraints involving the variable back into the queue.

    :param csp: The CSP problem
    :type csp: CSP
        
    :param last_assigned_var: The last variable assigned before propagation.
        None if no variable has been assigned yet (that is, we are performing 
        propagation before search starts).
    :type last_assigned_var: Variable

    :returns: a boolean indicating if the current assignment satisfies 
        all the constraints and a list of variable and value pairs pruned. 
    :rtype: boolean, List[(Variable, Value)]
    """
    queue = []
    prunings = []

    if last_assigned_var is None:
        # if no variable has been assigned, add all arcs <variable, constraint> to the queue
        for constraint in csp.get_all_cons():
            for var in constraint.get_scope():
                queue.append((var, constraint))
    else:
        # if a variable has been assigned, add only arcs involving that variable
        for constraint in csp.get_cons_with_var(last_assigned_var):
            for var in constraint.get_scope():
                if var != last_assigned_var:
                    queue.append((var, constraint))

    while queue:
        (var, constraint) = queue.pop(0)
        if revise(var, constraint, prunings):
            if var.cur_domain_size() == 0:
                # if a variables domain becomes empty, return False (failure)
                return False, prunings
            # add all other constraints involving var back to the queue
            for cons in csp.get_cons_with_var(var):
                if cons != constraint:
                    queue.append((var, cons))

    return True, prunings



def ord_mrv(csp):
    """
    Implement the Minimum Remaining Values (MRV) heuristic.
    Choose the next variable to assign based on MRV.

    If there is a tie, we will choose the first variable. 

    :param csp: A CSP problem
    :type csp: CSP

    :returns: the next variable to assign based on MRV

    """
    # stores variable with the fewest remaining values
    best_mvr = None 
    min_domain = float('inf') 

    # look through all variables in the CSP
    for var in csp.vars:
       # check if variable is unassigned
       if var.assignedValue is None:
           # calculate the current domain size (values in dom with True in curdom)
           domain_size = sum(1 for i in range(len(var.dom)) if var.curdom[i])

           # update mrv_var is this variable has fewer values in its domain
           if domain_size < min_domain:
              best_mvr = var
              min_domain = domain_size

    # return variable with the smallest domain
    return best_mvr


###############################################################################
# Do not modify the prop_BT function below
###############################################################################


def prop_BT(csp, last_assigned_var=None):
    """
    This is a basic propagator for plain backtracking search.

    Check if the current assignment satisfies all the constraints.
    Note that we only need to check all the fully instantiated constraints 
    that contain the last assigned variable.
    
    :param csp: The CSP problem
    :type csp: CSP

    :param last_assigned_var: The last variable assigned before propagation.
        None if no variable has been assigned yet (that is, we are performing 
        propagation before search starts).
    :type last_assigned_var: Variable

    :returns: a boolean indicating if the current assignment satisifes all the constraints 
        and a list of variable and value pairs pruned. 
    :rtype: boolean, List[(Variable, Value)]

    """
    
    # If we haven't assigned any variable yet, return true.
    if not last_assigned_var:
        return True, []
        
    # Check all the constraints that contain the last assigned variable.
    for c in csp.get_cons_with_var(last_assigned_var):

        # All the variables in the constraint have been assigned.
        if c.get_num_unassigned_vars() == 0:

            # get the variables
            vars = c.get_scope() 

            # get the list of values
            vals = []
            for var in vars: #
                vals.append(var.get_assigned_value())

            # check if the constraint is satisfied
            if not c.check(vals): 
                return False, []

    return True, []
