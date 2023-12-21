package use_case.generate_meal;

import app.custom_data.Range;
import org.junit.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;

public class GenerateMealUseCaseInteractorTest{

    @Test
    public void sucessTest(){
        GenerateMealOutputBoundary successPresenter = new GenerateMealOutputBoundary() {
            @Override
            public void prepareSuccessView(GenerateMealOutputData outputData) {

                //generating a number between 0 and 19 inclusive (picking one of the 20 meals randomly)
                int randomNum = (int)(Math.random() * 20);


                //Testing cal range
                double calRangeTotal = outputData.getMeals()[randomNum].getRecipe().getCalories();
                double servings =  outputData.getMeals()[randomNum].getRecipe().getServings();
                double calRangePerServing = calRangeTotal/servings;
                assertTrue(calRangePerServing >= 0 && calRangePerServing <= 300);


                //Testing Carb range
                double carbRangeTotal = outputData.getMeals()[randomNum].getRecipe().getTotalNutrients().getCarb().getQuantity();
                double carbRangePerServing = carbRangeTotal/servings;
                assertTrue(carbRangePerServing >= 0 && carbRangePerServing <= 100);

                //Testing Protein range
                double proteinRangeTotal = outputData.getMeals()[randomNum].getRecipe().getTotalNutrients().getProtein().getQuantity();
                double proteinRangePerServing = proteinRangeTotal/servings;
                assertTrue(proteinRangePerServing >= 0 && proteinRangePerServing <= 100);

                //Testing Fat range
                double fatRangeTotal = outputData.getMeals()[randomNum].getRecipe().getTotalNutrients().getFat().getQuantity();
                double fatRangePerServing = fatRangeTotal/servings;
                assertTrue(fatRangePerServing >= 0 && fatRangePerServing <= 40);

                //Testing health preferences
                List<String> healthPreferences = List.of("Peanut-Free");
                String[] healthPreferencesFromAPI = outputData.getMeals()[randomNum].getRecipe().getHealthLabels();
                assertTrue(Arrays.asList(healthPreferencesFromAPI).containsAll(healthPreferences));

                //Testing meal type
                String[] mealTypeFromAPI = outputData.getMeals()[randomNum].getRecipe().getMealType();
                assertTrue(Arrays.asList(mealTypeFromAPI).get(0).contains("lunch"));

                //Testing dish type
                List<String> dishType = List.of("main course");
                String[] dishTypeFromAPI = outputData.getMeals()[randomNum].getRecipe().getDishType();
                assertTrue(Arrays.asList(dishTypeFromAPI).containsAll(dishType));
            }


            @Override
            public void prepareFailView(String error) {
                fail(error);
            }
        };

        GenerateMealInputData inputData = new GenerateMealInputData(List.of("peanut-free"),
                List.of("Lunch"),
                List.of("Main course"),
                new Range<>(0, 300), //Cal range(per serving),
                new Range<>(0, 100), //Carb range(per serving)
                new Range<>(0, 100), //Protein range(per serving)
                new Range<>(0, 40)); //Fat range(per serving)
        GenerateMealInputBoundary interactor = new GenerateMealUseCaseInteractor(successPresenter);

        interactor.execute(inputData);
    }

    @Test
    public void noMealFoundFailTest(){
        GenerateMealOutputBoundary failPresenter = new GenerateMealOutputBoundary() {
            @Override
            public void prepareSuccessView(GenerateMealOutputData outputData) {
                assertEquals(0, outputData.getMeals().length);
            }

            @Override
            public void prepareFailView(String error) {
                assertEquals("No meals found, please try again.", error);
            }

        };

        GenerateMealInputData inputData = new GenerateMealInputData(List.of("peanut-free"),
                List.of("abc"),
                List.of("s"), //if mealType is not empty, and is invalid, it will return 0 meals found
                new Range<>(0, 300), //Cal range(per serving),
                new Range<>(0, 100), //Carb range(per serving)
                new Range<>(0, 100), //Protein range(per serving)
                new Range<>(0, 40)); //Fat range(per serving)
        GenerateMealInputBoundary interactor = new GenerateMealUseCaseInteractor(failPresenter);

        interactor.execute(inputData);
    }

    @Test
    public void badResponseTest(){
        GenerateMealOutputBoundary failPresenter = new GenerateMealOutputBoundary() {
            @Override
            public void prepareSuccessView(GenerateMealOutputData outputData) {

            }

            @Override
            public void prepareFailView(String error) {
                assertEquals("Error (Code 400).", error);
            }

        };

        GenerateMealInputData inputData = new GenerateMealInputData(List.of("peanut-free"),
                List.of("abc"), //invalid health preference
                List.of(""), //if mealType is empty, it will return 400 bad request
                new Range<>(0, 300), //Cal range(per serving),
                new Range<>(0, 100), //Carb range(per serving)
                new Range<>(0, 100), //Protein range(per serving)
                new Range<>(0, 40)); //Fat range(per serving)
        GenerateMealInputBoundary interactor = new GenerateMealUseCaseInteractor(failPresenter);

        interactor.execute(inputData);
    }

}