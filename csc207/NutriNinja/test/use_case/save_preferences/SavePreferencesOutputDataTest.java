package use_case.save_preferences;

import app.custom_data.Range;
import entity.NutrientRange;
import entity.UserPreferences;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;

public class SavePreferencesOutputDataTest {
    List<String> healthPreferences = new ArrayList<>(Arrays.asList("test1", "test2"));
    List<String> dishType = new ArrayList<>(Arrays.asList("test1", "test2"));
    Range<Integer> calorieRange = new Range<>(800, 1200);
    Range<Integer> fatRange = new Range<>(0, 30);
    Range<Integer> proteinRange = new Range<>(10, 50);
    Range<Integer> carbRange = new Range<>(10, 50);
    UserPreferences preferences = new UserPreferences(new NutrientRange(calorieRange, fatRange, proteinRange, carbRange), healthPreferences, dishType);
    SavePreferencesOutputData outputData = new SavePreferencesOutputData(preferences);

    @Test
    public void getMessage() {
        assertEquals("Preferences Saved!", outputData.getMessage());
    }

    @Test
    public void getUserPreferences() {
        assertEquals(preferences, outputData.getUserPreferences());
    }
}