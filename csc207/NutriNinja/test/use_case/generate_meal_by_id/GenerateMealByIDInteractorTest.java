package use_case.generate_meal_by_id;

import app.custom_data.Range;
import org.junit.Before;
import org.junit.Test;
import use_case.generate_meal.*;

import java.util.List;

import static org.junit.Assert.*;

public class GenerateMealByIDInteractorTest {

    @Test
    public void successTest() {
        GenerateMealByIDOutputBoundary successPresenter = new GenerateMealByIDOutputBoundary() {
            @Override
            public void prepareSuccessView(GenerateMealByIDOutputData outputData) {
                GenerateMealByIDOutputData.Recipe recipe = outputData.getRecipe();
                assertEquals("Seriously Asian: The Magic Of Miso Marination", recipe.getLabel());
                assertTrue(recipe.getImage().contains("ff5ec0deeb8f2c5a9ef2bcc55146783f"));
                assertEquals("Serious Eats", recipe.getSource());
                assertEquals("http://www.seriouseats.com/recipes/2009/08/miso-marination-asian-marinades-beef-fish.html", recipe.getUrl());
                assertEquals(1202.4841214990113, recipe.getCalories(), 0.0);
                assertEquals(6.0, recipe.getServings(), 0.0);
                assertArrayEquals(new String[]{
                        "Sugar-Conscious",
                        "Keto-Friendly",
                        "Dairy-Free",
                        "Gluten-Free",
                        "Wheat-Free",
                        "Egg-Free",
                        "Peanut-Free",
                        "Tree-Nut-Free",
                        "Fish-Free",
                        "Shellfish-Free",
                        "Pork-Free",
                        "Crustacean-Free",
                        "Celery-Free",
                        "Mustard-Free",
                        "Sesame-Free",
                        "Lupine-Free",
                        "Mollusk-Free",
                        "No oil added",
                        "Sulfite-Free",
                        "Kosher"}, recipe.getHealthLabels());
                assertArrayEquals(new String[]{"lunch/dinner"}, recipe.getMealType());

                GenerateMealByIDOutputData.Recipe.TotalNutrients totalNutrients = recipe.getTotalNutrients();
                GenerateMealByIDOutputData.Recipe.TotalNutrients.Nutrients protein = totalNutrients.getProtein();
                GenerateMealByIDOutputData.Recipe.TotalNutrients.Nutrients fat = totalNutrients.getFat();
                GenerateMealByIDOutputData.Recipe.TotalNutrients.Nutrients carb = totalNutrients.getCarb();

                assertEquals("Protein", protein.getLabel());
                assertEquals(159.2065112133297, protein.getQuantity(), 0.0);
                assertEquals("g", protein.getUnit());

                assertEquals("Fat", fat.getLabel());
                assertEquals(38.23585616216666, fat.getQuantity(), 0.0);
                assertEquals("g", fat.getUnit());

                assertEquals("Carbs", carb.getLabel());
                assertEquals(29.192299599296433, carb.getQuantity(), 0.0);
                assertEquals("g", carb.getUnit());
            }

            @Override
            public void prepareFailView(String error) {
                fail("Should have called prepareSuccessView");
            }
        };

        GenerateMealByIDInputData inputData = new GenerateMealByIDInputData("aaa542a6a01a6bf9a3e0658246c651af");
        GenerateMealByIDInputBoundary interactor = new GenerateMealByIDInteractor(successPresenter);

        interactor.execute(inputData);
    }

    @Test
    public void failTest() {
        GenerateMealByIDOutputBoundary failPresenter = new GenerateMealByIDOutputBoundary() {
            @Override
            public void prepareSuccessView(GenerateMealByIDOutputData outputData) {
                fail("Should have called prepareFailView.");
            }

            @Override
            public void prepareFailView(String error) {
                assertEquals("Error (Code 404).", error);
            }

        };

        GenerateMealByIDInputData inputData = new GenerateMealByIDInputData("123456789");
        GenerateMealByIDInputBoundary interactor = new GenerateMealByIDInteractor(failPresenter);

        interactor.execute(inputData);
    }
}