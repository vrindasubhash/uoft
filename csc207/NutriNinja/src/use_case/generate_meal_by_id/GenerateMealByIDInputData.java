package use_case.generate_meal_by_id;

public class GenerateMealByIDInputData {
    private final String mealID;

    public GenerateMealByIDInputData(String mealID) {
        this.mealID = mealID;
    }

    public String getMealID() {
        return mealID;
    }

}
