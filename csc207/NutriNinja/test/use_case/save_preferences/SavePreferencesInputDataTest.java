package use_case.save_preferences;

import app.custom_data.Range;
import entity.NutrientRange;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;

public class SavePreferencesInputDataTest {
    List<String> healthPreferences = new ArrayList<>(Arrays.asList("test1", "test2"));
    List<String> dishType = new ArrayList<>(Arrays.asList("test1", "test2"));
    Range<Integer> calorieRange = new Range<>(800, 1200);
    Range<Integer> fatRange = new Range<>(0, 30);
    Range<Integer> proteinRange = new Range<>(10, 50);
    Range<Integer> carbRange = new Range<>(10, 50);
    SavePreferencesInputData inputData = new SavePreferencesInputData(calorieRange,
            fatRange,
            proteinRange,
            carbRange,
            healthPreferences,
            dishType,
            "TestUser");


    @Test
    public void getNutrientRange() {
        assertEquals(calorieRange, inputData.getNutrientRange().getCalorieRange());
        assertEquals(fatRange, inputData.getNutrientRange().getFatRange());
        assertEquals(proteinRange, inputData.getNutrientRange().getProteinRange());
        assertEquals(carbRange, inputData.getNutrientRange().getCarbRange());
    }

    @Test
    public void getHealthPreferences() {
        assertEquals(healthPreferences, inputData.getHealthPreferences());
    }

    @Test
    public void getDietPreference() {
        assertEquals(dishType, inputData.getDishType());
    }

    @Test
    public void getUsername() {
        assertEquals("TestUser", inputData.getUsername());
    }
}