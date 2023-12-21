package use_case.generate_meal_by_id;

public interface GenerateMealByIDOutputBoundary {
    void prepareSuccessView(GenerateMealByIDOutputData outputData);

    void prepareFailView(String error);
}
