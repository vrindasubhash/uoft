from naive_bayes import naive_bayes_model
from naive_bayes import salary_variable_domains, salary_variable
from naive_bayes import explore

def test_explore():
    # Load the Bayesian Network model using the training data
    print("Loading Bayesian Network...")
    data_file = 'data/adult-test.csv'  # Use your dataset file here
    bayes_net = naive_bayes_model(data_file, salary_variable_domains, salary_variable)

    # Test each of the six questions in the explore function
    print("Testing explore function for all questions:")
    for question in range(1, 7):
        print(f"\nQuestion {question}:")
        try:
            result = explore(bayes_net, question)
            print(f"Result for Question {question}: {result:.2f}%")
        except Exception as e:
            print(f"Error testing Question {question}: {e}")

if __name__ == "__main__":
    test_explore()
