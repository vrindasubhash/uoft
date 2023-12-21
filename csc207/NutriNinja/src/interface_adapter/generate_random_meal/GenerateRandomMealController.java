package interface_adapter.generate_random_meal;

import app.custom_data.RandomRecipesList;
import use_case.generate_meal.GenerateMealInputBoundary;
import use_case.generate_meal_by_id.GenerateMealByIDInputBoundary;
import use_case.generate_meal_by_id.GenerateMealByIDInputData;
import use_case.generate_meal_by_id.GenerateMealByIDInteractor;

public class GenerateRandomMealController {
    final GenerateMealByIDInputBoundary generateMealByIDInteractor;

    public GenerateRandomMealController(GenerateMealByIDInputBoundary generateMealUseCaseInteractor) {
        this.generateMealByIDInteractor = generateMealUseCaseInteractor;
    }

    /**
     * This method picks a random meal from the list of meals and sends it to the use case by calling interactor.execute()
     */
    public void execute(){
        // Generate a random number between 0 and 19 inclusive
        int index = (int)(Math.random() * 20);

        String mealID = RandomRecipesList.randomRecipesList[index];

        GenerateMealByIDInputData inputData = new GenerateMealByIDInputData(mealID);
        generateMealByIDInteractor.execute(inputData);
    }

}
