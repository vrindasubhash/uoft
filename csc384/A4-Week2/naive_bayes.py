############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 4 Starter Code
## v1.0
############################################################

from bnetbase import Variable, Factor, BN
import csv


def normalize(factor):
    '''
    Normalize the factor such that its values sum to 1.
    Do not modify the input factor.

    :param factor: a Factor object. 
    :return: a new Factor object resulting from normalizing factor.
    '''
    total = sum(factor.values)
 
    # Check for zero total to avoid division by zero
    if total == 0:
        return None

    normalized_values = [v / total for v in factor.values]
    normalized_factor = Factor(factor.name, factor.scope)
    normalized_factor.values = normalized_values
    return normalized_factor
  

def restrict(factor, variable, value):
    '''
    Restrict a factor by assigning value to variable.
    Do not modify the input factor.

    :param factor: a Factor object.
    :param variable: the variable to restrict.
    :param value: the value to restrict the variable to
    :return: a new Factor object resulting from restricting variable to value.
             This new factor no longer has variable in it.
    ''' 
    # check if the variable is in the scope of the factor
    if variable not in factor.scope:
        return None
 
    # check if the value is in the variables domain
    if value not in variable.domain():
        return None

    # make a new scope without the restricted variable
    restricted_scope = [v for v in factor.get_scope() if v != variable]

    # initialize the restricted factor
    restricted_factor = Factor(f"{factor.name}_restricted_{variable.name}", restricted_scope)
   
    restricted_values = []

    for i in range(len(factor.values)):
        assignments = []
        temp_index = i
        for v in reversed(factor.scope):
            assignments.append(temp_index % v.domain_size())
            temp_index //= v.domain_size()
        assignments.reverse()

        if assignments[factor.scope.index(variable)] == variable.value_index(value):
            restricted_values.append(factor.values[i])

    restricted_factor.values = restricted_values
    return restricted_factor
 


def sum_out(factor, variable):
    '''
    Sum out a variable variable from factor factor.
    Do not modify the input factor.

    :param factor: a Factor object.
    :param variable: the variable to sum out.
    :return: a new Factor object resulting from summing out variable from the factor.
             This new factor no longer has variable in it.
    '''       
    # check if the variable is in the scope of the factor
    if variable not in factor.scope:
        return None

    # make new scope without the variable to be summed out
    summed_scope = [v for v in factor.get_scope() if v != variable]
    
    # initialize new factor
    summed_factor = Factor(f"{factor.name}_summed_{variable.name}", summed_scope)
    variable_index = factor.scope.index(variable)
    variable_domain_size = variable.domain_size()

    summed_values = [0] * len(summed_factor.values)
  
    for i in range(len(factor.values)):
        assignments = []
        temp_index = i
        for v in reversed(factor.scope):
            assignments.append(temp_index % v.domain_size())
            temp_index //= v.domain_size()
        assignments.reverse()

        summed_index = 0
        for j, v in enumerate(summed_scope):
            summed_index = summed_index * v.domain_size() + assignments[factor.scope.index(v)]

        summed_values[summed_index] += factor.values[i]

    summed_factor.values = summed_values
    return summed_factor


def multiply(factor_list):
    '''
    Multiply a list of factors together.
    Do not modify any of the input factors. 

    :param factor_list: a list of Factor objects.
    :return: a new Factor object resulting from multiplying all the factors in factor_list.
    ''' 
    if not factor_list:
        return None
    
    # determine the combined scope of all factors
    combined_scope = []
    for factor in factor_list:
        for var in factor.get_scope():
            if var not in combined_scope:
                combined_scope.append(var)
    
    # create the new factor with the combined scope
    new_factor = Factor("ResultFactor", combined_scope)
    
    # save current assignments of all variables in the combined scope
    saved_assignments = {var: var.get_assignment_index() for var in combined_scope}
    
    # generate all possible assignments for variables in the combined scope
    domains = [var.domain() for var in combined_scope]
    all_assignments = [[]]  
    
    for domain in domains:
        new_assignments = []
        for assignment in all_assignments:
            for value in domain:
                new_assignments.append(assignment + [value])
        all_assignments = new_assignments
    
    # iterate over each possible assignment
    for assignment in all_assignments:
        # assign the values to the variables
        for var, value in zip(combined_scope, assignment):
            var.set_assignment(value)
        
        # compute the product of all factor values for this assignment
        product = 1.0
        for factor in factor_list:
            product *= factor.get_value_at_current_assignments()
        
        # add the product to the new factor
        new_factor.add_value_at_current_assignment(product)
    
    # restore original assignments
    for var, index in saved_assignments.items():
        var.set_assignment_index(index)
    
    return new_factor
    

def ve(bayes_net, var_query, varlist_evidence): 
    '''
    Execute the variable elimination algorithm on the Bayesian network bayes_net
    to compute a distribution over the values of var_query given the 
    evidence provided by varlist_evidence. 

    :param bayes_net: a BN object.
    :param var_query: the query variable. we want to compute a distribution
                     over the values of the query variable.
    :param varlist_evidence: the evidence variables. Each evidence variable has 
                         its evidence set to a value from its domain 
                         using set_evidence.
    :return: a Factor object representing a distribution over the values
             of var_query. that is a list of numbers, one for every value
             in var_query's domain. These numbers sum to 1. The i-th number
             is the probability that var_query is equal to its i-th value given 
             the settings of the evidence variables.

    '''
    factors = bayes_net.factors()
     
    # convert varlist_evidence to a dictionary if it's a list
    if isinstance(varlist_evidence, list):
        varlist_evidence = {var: var.get_evidence() for var in varlist_evidence}

    # restrict factors based on evidence
    for var, val in varlist_evidence.items():
        factors = [restrict(factor, var, val) if var in factor.scope else factor for factor in factors]

    # eliminate variables not in query or evidence
    variables = bayes_net.variables()
    for var in variables:
        if var != var_query and var not in varlist_evidence:
            # find all factors that contain the current variable
            related_factors = [f for f in factors if var in f.scope]
            if related_factors:
                # multiply and sum out the variable
                new_factor = multiply(related_factors)
                new_factor = sum_out(new_factor, var)
                # replace old factors with the new one
                factors = [f for f in factors if f not in related_factors] + [new_factor]

    # multiply remaining factors and normalize
    final_factor = multiply(factors)
    return normalize(final_factor)
 

## The order of these domains is consistent with the order of the columns in the data set.
salary_variable_domains = {
"Work": ['Not Working', 'Government', 'Private', 'Self-emp'],
"Education": ['<Gr12', 'HS-Graduate', 'Associate', 'Professional', 'Bachelors', 'Masters', 'Doctorate'],
"Occupation": ['Admin', 'Military', 'Manual Labour', 'Office Labour', 'Service', 'Professional'],
"MaritalStatus": ['Not-Married', 'Married', 'Separated', 'Widowed'],
"Relationship": ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'],
"Race": ['White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other'],
"Gender": ['Male', 'Female'],
"Country": ['North-America', 'South-America', 'Europe', 'Asia', 'Middle-East', 'Carribean'],
"Salary": ['<50K', '>=50K']
}

salary_variable=Variable("Salary", ['<50K', '>=50K'])

def naive_bayes_model(data_file, variable_domains=salary_variable_domains, class_var=salary_variable):
    '''
    NaiveBayesModel returns a BN that is a Naive Bayes model that represents 
    the joint distribution of value assignments to variables in the given dataset.

    Remember a Naive Bayes model assumes P(X1, X2,.... XN, Class) can be represented as 
    P(X1|Class) * P(X2|Class) * .... * P(XN|Class) * P(Class).

    When you generated your Bayes Net, assume that the values in the SALARY column of 
    the dataset are the CLASS that we want to predict.

    Please name the factors as follows. If you don't follow these naming conventions, you will fail our tests.
    - The name of the Salary factor should be called "Salary" without the quotation marks.
    - The name of any other factor should be called "VariableName,Salary" without the quotation marks. 
      For example, the factor for Education should be called "Education,Salary".

    @return a BN that is a Naive Bayes model and which represents the given data set.
    '''
    ### READ IN THE DATA
    input_data = []
    with open(data_file, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None) #skip header row
        for row in reader:
            input_data.append(row)

    # map headers to variables
    variables = {header: Variable(header, variable_domains[header]) for header in headers}

    # initialize factors
    factors = []

    # compute the factor for the class variable (Salary)
    salary_index = headers.index("Salary")
    salary_counts = {value: 0 for value in variable_domains["Salary"]}

    for row in input_data:
        salary_counts[row[salary_index]] += 1

    total_count = sum(salary_counts.values())
    salary_factor = Factor("Salary", [variables["Salary"]])

    salary_probabilities = [[value, count / total_count] for value, count in salary_counts.items()]
    salary_factor.add_values(salary_probabilities)
    factors.append(salary_factor)

    # compute the factors for other variables
    for variable_name in headers:
        if variable_name == "Salary":
            continue

        variable = variables[variable_name]
        variable_index = headers.index(variable_name)

        # create a factor conditioned on Salary
        factor_name = f"{variable_name},Salary"
        variable_factor = Factor(factor_name, [variable, variables["Salary"]])

        # count co-occurrences of variable values with Salary values
        conditional_counts = {
            salary: {value: 0 for value in variable_domains[variable_name]} for salary in variable_domains["Salary"]
        }
        salary_totals = {salary: 0 for salary in variable_domains["Salary"]}

        for row in input_data:
            variable_value = row[variable_index]
            salary_value = row[salary_index]
            conditional_counts[salary_value][variable_value] += 1
            salary_totals[salary_value] += 1

        # calculate conditional probabilities
        conditional_probabilities = []
        for salary_value, variable_counts in conditional_counts.items():
            for variable_value, count in variable_counts.items():
                if salary_totals[salary_value] > 0:
                    probability = count / salary_totals[salary_value]
                else:
                    probability = 0
                conditional_probabilities.append([variable_value, salary_value, probability])

        # add the conditional probabilities to the factor
        variable_factor.add_values(conditional_probabilities)
        factors.append(variable_factor)

    # bayesian network to return
    return BN("NaiveBayesModel", list(variables.values()), factors)


def explore(bayes_net, question):
    '''    
    Return a probability given a Naive Bayes Model and a question number 1-6. 
    
    The questions are below: 
    1. What percentage of the women in the test data set does our model predict having a salary >= $50K? 
    2. What percentage of the men in the test data set does our model predict having a salary >= $50K? 
    3. What percentage of the women in the test data set satisfies the condition: P(S=">=$50K"|Evidence) is strictly greater than P(S=">=$50K"|Evidence,Gender)?
    4. What percentage of the men in the test data set satisfies the condition: P(S=">=$50K"|Evidence) is strictly greater than P(S=">=$50K"|Evidence,Gender)?
    5. What percentage of the women in the test data set with a predicted salary over $50K (P(Salary=">=$50K"|E) > 0.5) have an actual salary over $50K?
    6. What percentage of the men in the test data set with a predicted salary over $50K (P(Salary=">=$50K"|E) > 0.5) have an actual salary over $50K?

    @return a percentage (between 0 and 100)
    ''' 
    ### YOUR CODE HERE ###
    raise NotImplementedError


