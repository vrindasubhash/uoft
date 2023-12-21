package interface_adapter.generate_meal;

import java.net.URISyntaxException;
import java.util.List;
import app.custom_data.Range;
import use_case.generate_meal.GenerateMealInputBoundary;
import use_case.generate_meal.GenerateMealInputData;

public class GenerateMealController {
    final GenerateMealInputBoundary generateMealUseCaseInteractor;

    public GenerateMealController(GenerateMealInputBoundary generateMealUseCaseInteractor) {
        this.generateMealUseCaseInteractor = generateMealUseCaseInteractor;
    }

    /**
     * This method packs up the data from the view and sends it to the use case by calling interactor.execute()
     * @param healthPreferences: List of health preferences
     * @param mealType: List of meal types
     * @param dishType: List of dish types
     * @param calMin: Minimum calories
     * @param calMax: Maximum calories
     * @param carbMin: Minimum carbs
     * @param carbMax: Maximum carbs
     * @param proteinMin: Minimum protein
     * @param proteinMax: Maximum protein
     * @param fatMin: Minimum fat
     * @param fatMax: Maximum fat
     */
    public void execute(List<String> healthPreferences, List<String> mealType, List<String> dishType, int calMin, int calMax, int carbMin, int carbMax, int proteinMin, int proteinMax, int fatMin, int fatMax){
        Range<Integer> calRange = new Range<>(calMin, calMax);
        Range<Integer> carbRange = new Range<>(carbMin, carbMax);
        Range<Integer> proteinRange = new Range<>(proteinMin, proteinMax);
        Range<Integer> fatRange = new Range<>(fatMin, fatMax);
        GenerateMealInputData generateMealInputData = new GenerateMealInputData(
                healthPreferences,
                mealType,
                dishType,
                calRange,
                carbRange,
                proteinRange,
                fatRange
        );
        generateMealUseCaseInteractor.execute(generateMealInputData);
    }
}
