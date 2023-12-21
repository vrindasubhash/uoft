package use_case.generate_meal;

public interface GenerateMealOutputBoundary {
    void prepareSuccessView(GenerateMealOutputData outputData);

    void prepareFailView(String error);
}
