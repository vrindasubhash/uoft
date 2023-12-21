package use_case.generate_meal;


import java.util.List;
import app.custom_data.Range;

public class GenerateMealInputData {


    private final List<String> healthPreferences;
    private final List<String> mealType;
    private final List<String> dishType;
    private final Range<Integer> calRange;
    private final Range<Integer> carbRange;
    private final Range<Integer> proteinRange;
    private final Range<Integer> fatRange;

    public GenerateMealInputData(List<String> healthPreferences,
                                 List<String> mealType,
                                 List<String> dishType,
                                 Range<Integer> calRange,
                                 Range<Integer> carbRange,
                                 Range<Integer> proteinRange,
                                 Range<Integer> fatRange ){
        this.healthPreferences = healthPreferences;
        this.mealType = mealType;
        this.dishType = dishType;
        this.calRange = calRange;
        this.carbRange = carbRange;
        this.proteinRange = proteinRange;
        this.fatRange = fatRange;
    }

    public List<String> getHealthPreferences() {
        return healthPreferences;
    }

    public List<String> getMealType() {
        return mealType;
    }

    public List<String> getDishType() {
        return dishType;
    }

    public String getCalRange() {
        return calRange.getRangeString();
    }

    public String getCarbRange() {
        return carbRange.getRangeString();
    }

    public String getProteinRange() {
        return proteinRange.getRangeString();
    }

    public String getFatRange() {
        return fatRange.getRangeString();
    }

}
