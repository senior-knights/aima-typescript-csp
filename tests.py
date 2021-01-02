import itertools

from aima_python import csp, search
from schedule_logic import *

# Testing Search


def test_search():
    try:
        problem = search.Problem()
    except TypeError:
        print("0")

    problem = search.Problem("initial")
    assert problem.initial == "initial"
    assert problem.goal == None
    print("1")

    try:
        problem.actions(None)
    except NotImplementedError:
        print("2")

    try:
        problem.result(None, None)
    except NotImplementedError:
        print("3")

    assert problem.goal_test(None)

    problem.goal = 1
    assert not problem.goal_test(None)
    assert problem.goal_test(1)

    problem.goal = [1, 2]
    assert not problem.goal_test(None)
    assert problem.goal_test(2)
    print("4")

    assert problem.path_cost(1, None, None, None) == 2
    assert problem.path_cost(10, None, None, None) == 11
    print("5")

    try:
        problem.value(None)
    except NotImplementedError:
        print("6")

# some utilities to move at some point


def get_possible_domain_values(attribute_list):
    """Returns the cross-product of all values of attributes"""
    return list(itertools.product(*attribute_list))


def get_domains(variables, possible_domain_values):
    """Gives the same possible attribute values for each
    variable in the CSP. Not useful for every problem. Specific
    to the course scheduling problem."""
    domains = {}
    for variable in variables:
        domains[variable] = possible_domain_values
    return domains

# testing CSP


def test_csp():
    try:
        aCSP = csp.CSP()
    except TypeError:
        print("Pass throw on invalid CSP instantiation")

    # some values for testing
    variables = classes = ['cs108', 'cs112', 'cs212', 'cs214']
    faculty = ['norman', 'vanderlinden', 'adams']
    times = ['mwf800', 'mwf900']
    rooms = ['nh253', 'sb382']
    attribute_list = [times, rooms, faculty]
    possible_domain_values = get_possible_domain_values(attribute_list)
    domains = get_domains(variables, possible_domain_values)
    neighbors = get_neighbors(variables)

    # setup and now test with all four params
    aCSP = csp.CSP(variables, domains, neighbors, constraints)

    assert aCSP.initial == ()
    assert aCSP.goal == None
    assert aCSP.variables == variables
    assert aCSP.domains == domains
    assert aCSP.neighbors == neighbors
    assert aCSP.constraints == constraints
    assert aCSP.curr_domains == None
    assert aCSP.nassigns == 0

    print("Pass create CSP will four params")

    # test with no variables parameter
    aCSP = csp.CSP(None, domains, neighbors, constraints)

    assert aCSP.variables == variables
    assert aCSP.variables == list(domains.keys())

    assert aCSP.initial == ()
    assert aCSP.goal == None
    assert aCSP.domains == domains
    assert aCSP.neighbors == neighbors
    assert aCSP.constraints == constraints
    assert aCSP.curr_domains == None
    assert aCSP.nassigns == 0

    print("Pass create CSP with three params")

    # test assign
    assert aCSP.nassigns == 0
    assignment = {}
    first_class = variables[0]
    # Note: all of the domain values are the same for every variable in this example
    first_valid_attributes = domains[first_class][0]
    second_valid_assignments = domains[first_class][1]
    aCSP.assign(first_class, first_valid_attributes, assignment)
    assert assignment == {first_class: first_valid_attributes}
    assert aCSP.nassigns == 1

    # test reassign
    aCSP.assign(first_class, second_valid_assignments, assignment)
    assert assignment == {first_class: second_valid_assignments}
    # TODO: should this be 1?
    assert aCSP.nassigns == 2

    print("Pass CSP.assign()")

    assert aCSP.nassigns == 2
    aCSP.unassign(first_class, assignment)
    assert assignment == {}
    # assert aCSP.nassigns == 0 # TODO: Should this be 0 instead of 2?
    assert aCSP.nassigns == 2

    second_class, third_class = (variable for variable in variables[1:3])

    aCSP.assign(third_class, first_valid_attributes, assignment)
    aCSP.unassign(second_class, assignment)

    assert assignment == {third_class: first_valid_attributes}
    assert aCSP.nassigns == 3

    aCSP.unassign(third_class, assignment)

    assert assignment == {}
    # TODO: should this be 0?
    assert aCSP.nassigns == 3

    print("Pass CSP.unassign()")

    # test with no assignments

    assignment = {}
    aCSP = csp.CSP(None, domains, neighbors, constraints)
    assert aCSP.nconflicts(
        first_class, first_valid_attributes, assignment) == 0

    # test with two conflicting assignment (time and room)

    aCSP.assign(first_class, first_valid_attributes, assignment)
    aCSP.assign(second_class, second_valid_assignments, assignment)

    assert aCSP.nconflicts(
        first_class, first_valid_attributes, assignment) == 1

    aCSP.assign(second_class, first_valid_attributes, assignment)
    assert aCSP.nconflicts(
        first_class, first_valid_attributes, assignment) == 1

    # test with two non-conflicting assignments
    sixth_valid_attributes = domains[first_class][5]
    aCSP.assign(second_class, sixth_valid_attributes, assignment)
    assert aCSP.nconflicts(
        first_class, first_valid_attributes, assignment) == 0

    print("Pass CSP.nconflicts()")

    # test display
    assert aCSP.display(assignment) == print(assignment)

    print("Pass CSP.display()")

    # test conflicted vars
    # NOTE: this function needs to have all variables with a key in the assignment
    for variable in variables:
        assignment[variable] = first_valid_attributes
    assert aCSP.conflicted_vars(assignment) == variables
    assert len(aCSP.conflicted_vars(assignment)) == 4

    # change one of the conflicts
    assignment[first_class] = sixth_valid_attributes
    variables_copy = variables.copy()
    variables_copy.remove(first_class)
    assert aCSP.conflicted_vars(assignment) == variables_copy
    assert len(aCSP.conflicted_vars(assignment)) == 3

    # change back to conflict
    assignment[first_class] = second_valid_assignments
    assert aCSP.conflicted_vars(assignment) == variables
    assert len(aCSP.conflicted_vars(assignment)) == 4

    print("Pass CSP.conflicted_vars")


# TODO: can test the Problem class methods for the CSP class.
if __name__ == "__main__":
    # test_search()
    test_csp()
