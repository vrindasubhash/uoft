import unittest
from bnetbase import Variable, Factor, BN
from naive_bayes import normalize, restrict, sum_out, multiply, ve, naive_bayes_model, explore


class TestNaiveBayes(unittest.TestCase):

    def setUp(self):
        # Create sample variables and factors for testing
        self.salary_variable = Variable("Salary", ['<50K', '>=50K'])
        self.work_variable = Variable("Work", ['Not Working', 'Government', 'Private', 'Self-emp'])

        # Create a sample factor
        self.sample_factor = Factor("TestFactor", [self.salary_variable, self.work_variable])
        self.sample_factor.values = [0.1, 0.2, 0.3, 0.4, 0.15, 0.25, 0.35, 0.45]

        # Create the dataset
        self.test_csv_path = "adult-train_tiny.csv"
        with open(self.test_csv_path, "w") as f:
            f.write("""Work,Education,MaritalStatus,Occupation,Relationship,Race,Gender,Country,Salary
Private,Bachelors,Not-Married,Manual Labour,Not-in-family,Asian-Pac-Islander,Male,North-America,<50K
Private,Bachelors,Not-Married,Manual Labour,Not-in-family,Asian-Pac-Islander,Male,North-America,<50K
Private,Masters,Not-Married,Manual Labour,Not-in-family,Asian-Pac-Islander,Male,North-America,<50K
Private,Masters,Not-Married,Manual Labour,Not-in-family,Asian-Pac-Islander,Female,North-America,<50K
Private,Masters,Not-Married,Manual Labour,Not-in-family,Asian-Pac-Islander,Female,North-America,<50K
Private,Masters,Not-Married,Manual Labour,Not-in-family,Amer-Indian-Eskimo,Male,South-America,<50K
Private,Bachelors,Not-Married,Manual Labour,Not-in-family,Asian-Pac-Islander,Male,North-America,>=50K
Private,Bachelors,Not-Married,Manual Labour,Not-in-family,Asian-Pac-Islander,Male,North-America,>=50K
Private,Bachelors,Married,Manual Labour,Husband,Asian-Pac-Islander,Male,North-America,>=50K
Private,Bachelors,Married,Manual Labour,Wife,Asian-Pac-Islander,Female,North-America,>=50K
""")

        # Create the Bayesian Network
        self.bayes_net = naive_bayes_model(self.test_csv_path)

    def test_normalize(self):
        normalized_factor = normalize(self.sample_factor)
        expected_values = [val / sum(self.sample_factor.values) for val in self.sample_factor.values]
        self.assertAlmostEqual(sum(normalized_factor.values), 1.0, places=6)
        for i, value in enumerate(normalized_factor.values):
            self.assertAlmostEqual(value, expected_values[i], places=6)

    def test_restrict(self):
        restricted_factor = restrict(self.sample_factor, self.salary_variable, '<50K')
        self.assertEqual(len(restricted_factor.scope), 1)  # "Work" remains
        self.assertEqual(restricted_factor.values, [0.1, 0.2, 0.3, 0.4])

    def test_sum_out(self):
        summed_factor = sum_out(self.sample_factor, self.salary_variable)
        expected_values = [0.25, 0.45, 0.65, 0.85]
        for i, value in enumerate(summed_factor.values):
            self.assertAlmostEqual(value, expected_values[i], places=6)

    def test_multiply(self):
        factor1 = Factor("Factor1", [self.salary_variable])
        factor1.values = [0.3, 0.7]
        factor2 = Factor("Factor2", [self.salary_variable])
        factor2.values = [0.6, 0.4]
        product_factor = multiply([factor1, factor2])
        expected_values = [0.18, 0.28]
        for i, value in enumerate(product_factor.values):
            self.assertAlmostEqual(value, expected_values[i], places=6)

    def test_ve(self):
        salary_variable = Variable("Salary", ['<50K', '>=50K'])
        salary_factor = Factor("Salary", [salary_variable])
        salary_factor.values = [0.6, 0.4]
        bayes_net = BN("TestNet", [salary_variable], [salary_factor])
        result_factor = ve(bayes_net, salary_variable, [])
        self.assertEqual(result_factor.values, [0.6, 0.4])

    def test_naive_bayes_model(self):
        bayes_net = self.bayes_net
        self.assertIn("Salary", [factor.name for factor in bayes_net.factors()])
        self.assertIn("Work,Salary", [factor.name for factor in bayes_net.factors()])
        self.assertEqual(len(bayes_net.variables()), 9)

    # def test_explore(self):
    #     # Question 1
    #     result = explore(self.bayes_net, 1)
    #     print(f"Q1: Percentage of women predicted >= $50K: {result}%")
    #     self.assertAlmostEqual(result, 33.33, places=2)

    #     # Question 2
    #     result = explore(self.bayes_net, 2)
    #     print(f"Q2: Percentage of men predicted >= $50K: {result}%")
    #     self.assertAlmostEqual(result, 14.29, places=2)

    #     # Question 3
    #     result = explore(self.bayes_net, 3)
    #     print(f"Q3: Percentage of women satisfying P(Salary >= $50K | E) > P(Salary >= $50K | E, Gender): {result}%")
    #     self.assertAlmostEqual(result, 33.33, places=2)

    #     # Question 4
    #     result = explore(self.bayes_net, 4)
    #     print(f"Q4: Percentage of men satisfying P(Salary >= $50K | E) > P(Salary >= $50K | E, Gender): {result}%")
    #     self.assertAlmostEqual(result, 14.29, places=2)  # Updated expectation

    #     # Question 5
    #     result = explore(self.bayes_net, 5)
    #     print(f"Q5: Percentage of women with predicted >= $50K and actual >= $50K: {result}%")
    #     self.assertAlmostEqual(result, 33.33, places=2)

    #     # Question 6
    #     result = explore(self.bayes_net, 6)
    #     print(f"Q6: Percentage of men with predicted >= $50K and actual >= $50K: {result}%")
    #     self.assertAlmostEqual(result, 100.0, places=2)


if __name__ == "__main__":
    unittest.main()
