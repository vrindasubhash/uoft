from naive_bayes import naive_bayes_model
from bnetbase import Variable, Factor, BN

# Define a simple dataset
TEST_CSV = "test_dataset.csv"
TEST_DATA = """Work,Education,MaritalStatus,Occupation,Relationship,Race,Gender,Country,Salary
Private,Bachelors,Married,Professional,Husband,White,Male,North-America,>=50K
Private,Masters,Not-Married,Professional,Wife,Asian-Pac-Islander,Female,Asia,>=50K
Self-emp,HS-Graduate,Married,Manual Labour,Husband,White,Male,Europe,<50K
Private,HS-Graduate,Not-Married,Service,Not-in-family,Black,Male,North-America,<50K
Government,Bachelors,Married,Admin,Husband,White,Male,Europe,>=50K
"""

# Save the test data to a CSV file
with open(TEST_CSV, "w", encoding="utf-8") as f:
    f.write(TEST_DATA)

# Define variable domains
TEST_VARIABLE_DOMAINS = {
    "Work": ['Private', 'Self-emp', 'Government'],
    "Education": ['Bachelors', 'Masters', 'HS-Graduate'],
    "MaritalStatus": ['Married', 'Not-Married'],
    "Occupation": ['Professional', 'Manual Labour', 'Service', 'Admin'],
    "Relationship": ['Husband', 'Wife', 'Not-in-family'],
    "Race": ['White', 'Asian-Pac-Islander', 'Black'],
    "Gender": ['Male', 'Female'],
    "Country": ['North-America', 'Europe', 'Asia'],
    "Salary": ['<50K', '>=50K']
}

# Test Naive Bayes Model
def test_naive_bayes_model():
    # Create the Bayesian network
    salary_variable = Variable("Salary", TEST_VARIABLE_DOMAINS["Salary"])
    bayes_net = naive_bayes_model(TEST_CSV, TEST_VARIABLE_DOMAINS, salary_variable)

    # Debugging: Inspect factors
    print("\nWork,Salary Factor Table:")
    work_salary_factor = next(f for f in bayes_net.factors() if f.name == "Work,Salary")
    work_salary_factor.print_table()

    # Debugging: Inspect grouped_counts and class_totals
    # These are printed directly from the naive_bayes_model implementation
    # If not printed, add these lines inside naive_bayes_model:
    # print(f"Grouped Counts: {grouped_counts}")
    # print(f"Class Totals: {class_totals}")

    # Test cases for P(Salary)
    salary_factor = next(f for f in bayes_net.factors() if f.name == "Salary")
    print("\nSalary Factor Table:")
    salary_factor.print_table()

    # Validate probabilities for P(Salary)
    assert salary_factor.get_value(['<50K']) == 2 / 5, f"Expected P(Salary=<50K)=0.4, but got {salary_factor.get_value(['<50K'])}"
    assert salary_factor.get_value(['>=50K']) == 3 / 5, f"Expected P(Salary>=50K)=0.6, but got {salary_factor.get_value(['>=50K'])}"

    # Validate probabilities for P(Work | Salary)
    print("\nValidating Work | Salary Probabilities:")
    assert work_salary_factor.get_value(['Private', '<50K']) == 1 / 2, "P(Work=Private | Salary=<50K) incorrect"
    assert work_salary_factor.get_value(['Private', '>=50K']) == 2 / 3, "P(Work=Private | Salary>=50K) incorrect"
    assert work_salary_factor.get_value(['Government', '>=50K']) == 1 / 3, "P(Work=Government | Salary>=50K) incorrect"

    education_salary_factor = next(f for f in bayes_net.factors() if f.name == "Education,Salary")
    assert education_salary_factor.get_value(['Bachelors', '>=50K']) == 2 / 3, "P(Education=Bachelors | Salary>=50K) incorrect"
    assert education_salary_factor.get_value(['HS-Graduate', '<50K']) == 1, "P(Education=HS-Graduate | Salary=<50K) incorrect"


    print("\nAll tests passed!")

if __name__ == "__main__":
    test_naive_bayes_model()
