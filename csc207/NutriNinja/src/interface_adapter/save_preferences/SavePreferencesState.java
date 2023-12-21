package interface_adapter.save_preferences;
import java.util.ArrayList;
import java.util.List;

import app.custom_data.Range;
import entity.NutrientRange;

public class SavePreferencesState {
    private NutrientRange nutrientRange = new NutrientRange(new Range<>(0, 10000), new Range<>(0, 10000), new Range<>(0, 10000), new Range<>(0, 10000));
    private List<String> healthPreferences = new ArrayList<>();
    private List<String> dishType = new ArrayList<>();
    private List<String> mealType = new ArrayList<>();
    private String username = "";

    public SavePreferencesState(SavePreferencesState copy) {
        nutrientRange = copy.nutrientRange;
        healthPreferences = copy.healthPreferences;
        dishType = copy.dishType;
        mealType = copy.mealType;
        username = copy.username;;
    }

    // Because of the previous copy constructor, the default constructor must be explicit.
    public SavePreferencesState() {}

    public NutrientRange getNutrientRange() {
        return nutrientRange;
    }
    public List<String> getHealthPreferences() {
        return healthPreferences;
    }
    public List<String> getDishType() {
        return dishType;
    }
    public List<String> getMealType() {return mealType;}
    public String getUsername() {return username;}

    public void setNutrientRange(NutrientRange nutrientRange) {
        this.nutrientRange = nutrientRange;
    }
    public void setHealthPreferences(List<String> healthPreferences) {this.healthPreferences = healthPreferences;}
    public void setDishType(List<String> dishType) {this.dishType = dishType;}
    public void setMealType(List<String> mealType) {this.mealType = mealType;}
    public void setUsername(String username) {this.username = username;}


}

