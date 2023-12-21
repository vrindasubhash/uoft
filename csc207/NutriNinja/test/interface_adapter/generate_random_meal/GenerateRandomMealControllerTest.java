package interface_adapter.generate_random_meal;

import app.custom_data.RandomRecipesList;
import org.junit.Test;
import use_case.generate_meal_by_id.GenerateMealByIDInputBoundary;
import use_case.generate_meal_by_id.GenerateMealByIDInputData;

import java.util.Random;

import static org.junit.Assert.*;

public class GenerateRandomMealControllerTest {
    @Test
    public void execute() {
        GenerateRandomMealController generateRandomMealController = new GenerateRandomMealController(
                new GenerateMealByIDInputBoundary() {
                    @Override
                    public void execute(GenerateMealByIDInputData inputData) {
                        boolean inRecipeList = false;
                        String[] recipes = RandomRecipesList.randomRecipesList;
                        String selectedRecipe = inputData.getMealID();

                        for (String recipe : recipes) {
                            if (recipe.equals(selectedRecipe)) {
                                inRecipeList = true;
                                break;
                            }
                        }

                        assertTrue(inRecipeList);
                    }
                }
        );

        for (int i = 0; i < 100; i++) {
            generateRandomMealController.execute();
        }
    }
}