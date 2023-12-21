package interface_adapter.save_preferences;
import java.util.List;

import app.custom_data.Range;
import entity.NutrientRange;
import use_case.save_preferences.SavePreferencesInputBoundary;
import use_case.save_preferences.SavePreferencesInputData;

public class SavePreferencesController {
    final SavePreferencesInputBoundary saveUseCaseInteractor;
    public SavePreferencesController(SavePreferencesInputBoundary saveUseCaseInteractor) {
        this.saveUseCaseInteractor = saveUseCaseInteractor;
    }

    /**
     * Passes the SavePreferencesInputData to the SavePreferencesInteractor
     * @param calorieRange
     * @param fatRange
     * @param proteinRange
     * @param carbRange
     * @param healthPreferences
     * @param dishType
     * @param username
     */
    public void execute(Range<Integer> calorieRange,
                        Range<Integer> fatRange,
                        Range<Integer> proteinRange,
                        Range<Integer> carbRange, List<String> healthPreferences,
                        List<String> dishType, String username) {
        SavePreferencesInputData savePreferencesInputData = new SavePreferencesInputData(calorieRange,
                fatRange,
                proteinRange,
                carbRange, healthPreferences, dishType, username);
        saveUseCaseInteractor.execute(savePreferencesInputData);
    }
}
