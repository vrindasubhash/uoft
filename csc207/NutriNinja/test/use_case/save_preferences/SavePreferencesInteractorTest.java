package use_case.save_preferences;

import app.custom_data.Range;
import data_access.MemoryUserDataAccessObject;
import entity.CommonUser;
import entity.NutrientRange;
import entity.User;
import org.junit.Before;
import org.junit.Test;
import entity.CommonUserFactory;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;

public class SavePreferencesInteractorTest {
    MemoryUserDataAccessObject userDataAccessObject;
    List<String> healthPreferences = new ArrayList<>(Arrays.asList("test1", "test2"));
    List<String> dishType = new ArrayList<>(Arrays.asList("test1", "test2"));
    Range<Integer> calorieRange = new Range<>(800, 1200);
    Range<Integer> fatRange = new Range<>(0, 30);
    Range<Integer> proteinRange = new Range<>(10, 50);
    Range<Integer> carbRange = new Range<>(10, 50);


    @Before
    public void setUp(){
        this.userDataAccessObject = new MemoryUserDataAccessObject();
        User user = new CommonUserFactory().create("TestUser", "TestPass");
        this.userDataAccessObject.saveUser(user);
    }
    @Test
    public void successTest() {
        SavePreferencesOutputBoundary successPresenter = outputData -> {
            assertEquals("Preferences Saved!", outputData.getMessage());
            assertEquals(healthPreferences, outputData.getUserPreferences().getHealthPreferences());
            assertEquals(calorieRange, outputData.getUserPreferences().getNutrientRange().getCalorieRange());
            assertEquals(fatRange, outputData.getUserPreferences().getNutrientRange().getFatRange());
            assertEquals(proteinRange, outputData.getUserPreferences().getNutrientRange().getProteinRange());
            assertEquals(carbRange, outputData.getUserPreferences().getNutrientRange().getCarbRange());
            assertEquals(dishType, outputData.getUserPreferences().getDishType());
        };
        SavePreferencesInputData inputData = new SavePreferencesInputData(calorieRange, fatRange, proteinRange, carbRange,
                healthPreferences, dishType, "TestUser") ;
        SavePreferencesInputBoundary interactor = new SavePreferencesInteractor(
                userDataAccessObject, successPresenter);
        interactor.execute(inputData);
    }
}