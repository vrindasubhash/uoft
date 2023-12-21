package interface_adapter.generate_meal;

public class GenerateMealState {

    public String getMealName() {
        return mealName;
    }

    public void setMealName(String meal_label) {
        this.mealName = meal_label;
    }

    public String getImageURL() {
        return imageUrl;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }

    public double getMealCalories() {
        return mealCalories;
    }

    public void setMealCalories(double mealCalories) {
        this.mealCalories = mealCalories;
    }

    public double getMealProtein() {
        return mealProtein;
    }

    public void setMealProtein(double mealProtein) {
        this.mealProtein = mealProtein;
    }

    public double getMealCarbs() {
        return mealCarbs;
    }

    public void setMealCarbs(double mealCarbs) {
        this.mealCarbs = mealCarbs;
    }

    public double getMealFat() {
        return mealFat;
    }

    public void setMealFat(double mealFat) {
        this.mealFat = mealFat;
    }

    public String getIngredientsLabel() {
        return ingredientsLabel;
    }

    public void setIngredientsLabel(String ingredientsLabel) {
        this.ingredientsLabel = ingredientsLabel;
    }

    public String getRecipeURL() {
        return recipeUrl;
    }

    public void setRecipeUrl(String recipeUrl) {
        this.recipeUrl = recipeUrl;
    }

    public String getRecipeSource() {
        return recipeSource;
    }

    public void setRecipeSource(String recipe_source) {
        this.recipeSource = recipe_source;
    }

    public String getAPIError() {
        return APIError;
    }

    public void setAPIError(String APIError) {
        this.APIError = APIError;
    }

    public double getServings() {
        return servings;
    }

    public void setServings(double servings) {
        this.servings = servings;
    }


    public String mealName = "";

    public double servings = 0;
    public String imageUrl = ""; //URL of image
    public double mealCalories = 0;
    public double mealProtein = 0;
    public double mealCarbs = 0;
    public double mealFat = 0;


    //INGREDIENTS
    public String ingredientsLabel = "";


    //Recipe
    public String recipeUrl = ""; //url of recipe
    public String recipeSource = ""; //source of recipe

    //Error
    public String APIError = null;

    public GenerateMealState(GenerateMealState copy){
        this.mealName = copy.mealName;
        this.imageUrl = copy.imageUrl;
        this.mealCalories = copy.mealCalories;
        this.mealProtein = copy.mealProtein;
        this.mealCarbs = copy.mealCarbs;
        this.mealFat = copy.mealFat;
        this.ingredientsLabel = copy.ingredientsLabel;
        this.recipeUrl = copy.recipeUrl;
        this.recipeSource =copy.recipeSource;
        this.APIError = copy.APIError;
        this.servings = copy.servings;
    }

    //Explicit default constructor
    public GenerateMealState(){
    }


}
