from bnetbase import Factor, Variable, BN
from naive_bayes import naive_bayes_model

# Step 1: Create a test CSV file
def create_test_csv():
    test_csv_content = """Work,Education,MaritalStatus,Occupation,Relationship,Race,Gender,Country,Salary
Private,Bachelors,Not-Married,Manual Labour,Not-in-family,Asian-Pac-Islander,Male,North-America,>=50K
Private,Bachelors,Not-Married,Manual Labour,Not-in-family,Asian-Pac-Islander,Male,North-America,<50K
Private,Masters,Not-Married,Manual Labour,Not-in-family,Asian-Pac-Islander,Male,North-America,>=50K
Private,Masters,Not-Married,Manual Labour,Not-in-family,Asian-Pac-Islander,Female,North-America,<50K
"""
    with open("test_dataset.csv", "w") as f:
        f.write(test_csv_content)

# Step 2: Define variable domains
salary_variable_domains = {
    "Work": ["Private", "Government", "Self-emp", "Not Working"],
    "Education": ["Bachelors", "Masters", "Doctorate"],
    "MaritalStatus": ["Not-Married", "Married"],
    "Occupation": ["Manual Labour", "Office Labour"],
    "Relationship": ["Not-in-family", "Husband", "Wife"],
    "Race": ["Asian-Pac-Islander", "Amer-Indian-Eskimo"],
    "Gender": ["Male", "Female"],
    "Country": ["North-America", "South-America"],
    "Salary": ["<50K", ">=50K"]
}

salary_variable = Variable("Salary", salary_variable_domains["Salary"])

# Step 3: Test the naive_bayes_model function
def test_naive_bayes_model():
    create_test_csv()  # Create the test dataset

    # Load the Bayesian Network
    bayes_net = naive_bayes_model("test_dataset.csv", salary_variable_domains, salary_variable)

    # Print all factors in the Bayesian Network
    print("\nBayesian Network Factors:")
    for factor in bayes_net.factors():
        print(f"\nFactor: {factor.name}")
        factor.print_table()

    # Programmatic checks for expected probabilities
    # Retrieve the Salary factor
    salary_factor = next(f for f in bayes_net.factors() if f.name == "Salary")
    assert abs(salary_factor.get_value(["<50K"]) - 0.5) < 1e-6, "P(Salary=<50K) mismatch!"
    assert abs(salary_factor.get_value([">=50K"]) - 0.5) < 1e-6, "P(Salary>=50K) mismatch!"

    # Retrieve the Work,Salary factor
    work_salary_factor = next(f for f in bayes_net.factors() if f.name == "Work,Salary")
    assert abs(work_salary_factor.get_value(["Private", "<50K"]) - 1.0) < 1e-6, "P(Work=Private | Salary=<50K) mismatch!"
    assert abs(work_salary_factor.get_value(["Private", ">=50K"]) - 1.0) < 1e-6, "P(Work=Private | Salary>=50K) mismatch!"

    # Retrieve the Gender,Salary factor
    gender_salary_factor = next(f for f in bayes_net.factors() if f.name == "Gender,Salary")
    assert abs(gender_salary_factor.get_value(["Male", "<50K"]) - 0.5) < 1e-6, "P(Gender=Male | Salary=<50K) mismatch!"
    assert abs(gender_salary_factor.get_value(["Male", ">=50K"]) - 1.0) < 1e-6, "P(Gender=Male | Salary>=50K) mismatch!"
    assert abs(gender_salary_factor.get_value(["Female", "<50K"]) - 0.5) < 1e-6, "P(Gender=Female | Salary=<50K) mismatch!"
    assert abs(gender_salary_factor.get_value(["Female", ">=50K"]) - 0.0) < 1e-6, "P(Gender=Female | Salary>=50K) mismatch!"

    print("All tests passed!")

# Run the test
if __name__ == "__main__":
    test_naive_bayes_model()
