package interface_adapter.generate_meal;

import interface_adapter.ViewManagerModel;
import use_case.generate_meal.GenerateMealOutputBoundary;
import use_case.generate_meal.GenerateMealOutputData;

import java.util.Arrays;

public class GenerateMealPresenter implements GenerateMealOutputBoundary {

    private ViewManagerModel viewManagerModel;
    private GenerateMealViewModel generateMealViewModel;

    public  GenerateMealPresenter(ViewManagerModel viewManagerModel, GenerateMealViewModel generateMealViewModel) {
        this.viewManagerModel = viewManagerModel;
        this.generateMealViewModel = generateMealViewModel;
    }

    /**
     * This method packs up the data from the use case interactor and prepares the successes state for the view model
     * @param outputData: The output data for generate meal view, which is the meal data
     */
    @Override
    public void prepareSuccessView(GenerateMealOutputData outputData) {
        GenerateMealState generateMealState = generateMealViewModel.getState();

        int index = (int)(Math.random() * (double)outputData.getTo());

        generateMealState.setMealName(outputData.getMeals()[index].getRecipe().getLabel());
        generateMealState.setImageUrl(outputData.getMeals()[index].getRecipe().getImage());
        generateMealState.setMealCalories(outputData.getMeals()[index].getRecipe().getCalories());
        generateMealState.setMealProtein(outputData.getMeals()[index].getRecipe().getTotalNutrients().getProtein().getQuantity());
        generateMealState.setMealCarbs(outputData.getMeals()[index].getRecipe().getTotalNutrients().getCarb().getQuantity());
        generateMealState.setMealFat(outputData.getMeals()[index].getRecipe().getTotalNutrients().getFat().getQuantity());
        generateMealState.setIngredientsLabel(Arrays.toString(outputData.getMeals()[index].getRecipe().getIngredientLines()));
        generateMealState.setRecipeSource(outputData.getMeals()[index].getRecipe().getSource());
        generateMealState.setRecipeUrl(outputData.getMeals()[index].getRecipe().getUrl());
        generateMealState.setServings(outputData.getMeals()[index].getRecipe().getServings());
        generateMealState.setAPIError(null);

        this.generateMealViewModel.setState(generateMealState);
        this.generateMealViewModel.firePropertyChanged();

        this.viewManagerModel.setActiveView(generateMealViewModel.getViewName());
        this.viewManagerModel.firePropertyChanged();

    }

    /**
     * This method packs up the data from the use case interactor and prepares the fail state for the view model
     * @param error: The error message from the API call
     */
    @Override
    public void prepareFailView(String error) {
        GenerateMealState generateMealState = generateMealViewModel.getState();
        generateMealState.setAPIError(error);

        this.generateMealViewModel.setState(generateMealViewModel.getState());
        generateMealViewModel.firePropertyChanged();
    }
}
