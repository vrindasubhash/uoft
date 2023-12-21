package app;

import interface_adapter.ViewManagerModel;
import interface_adapter.generate_meal.GenerateMealController;
import interface_adapter.generate_meal.GenerateMealPresenter;
import interface_adapter.generate_meal.GenerateMealViewModel;
import interface_adapter.generate_random_meal.GenerateRandomMealController;
import interface_adapter.generate_random_meal.GenerateRandomMealPresenter;
import interface_adapter.save_preferences.SavePreferencesController;
import interface_adapter.save_preferences.SavePreferencesViewModel;
import use_case.generate_meal.GenerateMealInputBoundary;
import use_case.generate_meal.GenerateMealOutputBoundary;
import use_case.generate_meal.GenerateMealUseCaseInteractor;
import use_case.generate_meal_by_id.GenerateMealByIDInputBoundary;
import use_case.generate_meal_by_id.GenerateMealByIDInteractor;
import use_case.generate_meal_by_id.GenerateMealByIDOutputBoundary;
import use_case.save_preferences.SavePreferencesDataAccessInterface;
import view.GenerateMealView;

import javax.swing.*;
import java.io.IOException;

public class MealViewFactory {

    private MealViewFactory() {}

    public static GenerateMealView create(
            ViewManagerModel viewManagerModel, GenerateMealViewModel generateMealViewModel, SavePreferencesViewModel savePreferencesViewModel, SavePreferencesDataAccessInterface savePreferencesDataAccessObject) {

        try {
            GenerateMealController generateMealController = createGenerateMealUseCase(viewManagerModel, generateMealViewModel);
            SavePreferencesController savePreferencesController = PreferencesViewFactory.createSavePreferencesUseCase(viewManagerModel, savePreferencesViewModel, savePreferencesDataAccessObject);
            GenerateRandomMealController generateRandomMealController = createGenerateRandomMealUseCase(viewManagerModel, generateMealViewModel);
            return new GenerateMealView(generateMealViewModel, savePreferencesViewModel, generateMealController, savePreferencesController, generateRandomMealController);

        } catch (IOException e) {
            JOptionPane.showMessageDialog(null, "Image Failed To Load.");
        }

        return null;
    }


    public static GenerateMealController createGenerateMealUseCase (ViewManagerModel viewManagerModel, GenerateMealViewModel generateMealViewModel){
        GenerateMealOutputBoundary generateMealOutputboundary = new GenerateMealPresenter(viewManagerModel, generateMealViewModel);
        GenerateMealInputBoundary generateMealInputBoundary  = new GenerateMealUseCaseInteractor(generateMealOutputboundary);

        return new GenerateMealController(generateMealInputBoundary);
    }


    public static GenerateRandomMealController createGenerateRandomMealUseCase (ViewManagerModel viewManagerModel, GenerateMealViewModel generateMealViewModel){
        GenerateMealByIDOutputBoundary generateMealOutputboundary = new GenerateRandomMealPresenter(viewManagerModel, generateMealViewModel);
        GenerateMealByIDInputBoundary generateMealByIDInputBoundary  = new GenerateMealByIDInteractor(generateMealOutputboundary);

        return new GenerateRandomMealController(generateMealByIDInputBoundary);
    }




}
