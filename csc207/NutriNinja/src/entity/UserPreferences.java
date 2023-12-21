package entity;

import java.util.List;

public class UserPreferences {
    private NutrientRange nutrientRange;
    private List<String> healthPreferences;
    private List<String> dishType;


    public UserPreferences(NutrientRange nutrientRange, List<String> healthPreferences, List<String> dishType) {
        this.nutrientRange = nutrientRange;
        this.healthPreferences = healthPreferences;
        this.dishType = dishType;
    }

    public NutrientRange getNutrientRange() {
        return nutrientRange;
    }

    public void setNutrientRange(NutrientRange nutrientRange) {
        this.nutrientRange = nutrientRange;
    }

    public List<String> getHealthPreferences() {
        return healthPreferences;
    }

    public void setHealthPreferences(List<String> healthPreferences) {
        this.healthPreferences = healthPreferences;
    }

    public List<String> getDishType() {
        return dishType;
    }

    public void setDishType(List<String> dishType) {
        this.dishType = dishType;
    }

}
