package use_case.save_preferences;

import app.custom_data.Range;
import entity.NutrientRange;

import java.util.List;

public class SavePreferencesInputData {

    private final NutrientRange nutrientRange;
    private final List<String> healthPreferences;

    private final List<String> dishType;

    private final String username;


    public SavePreferencesInputData(Range<Integer> calorieRange,
                                    Range<Integer> fatRange,
                                    Range<Integer> proteinRange,
                                    Range<Integer> carbRange,
                                    List<String> healthPreferences,
                                    List<String> dishType,
                                    String username) {
        this.nutrientRange = new NutrientRange(calorieRange, fatRange, proteinRange, carbRange);
        this.healthPreferences = healthPreferences;
        this.dishType = dishType;
        this.username = username;
    }

    NutrientRange getNutrientRange() {
        return this.nutrientRange;
    }

    List<String> getHealthPreferences(){
        return this.healthPreferences;
    }

    List<String> getDishType(){
        return this.dishType;
    }

    String getUsername(){return this.username;}

}
