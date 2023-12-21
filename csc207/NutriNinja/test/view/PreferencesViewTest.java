package view;

import app.PreferencesViewFactory;
import app.custom_data.Range;
import data_access.FileUserDataAccessObject;
import entity.*;
import interface_adapter.ViewManagerModel;
import interface_adapter.generate_meal.GenerateMealViewModel;
import interface_adapter.save_preferences.SavePreferencesViewModel;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import entity.NutrientRange;

import javax.swing.*;

import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

import static org.junit.Assert.*;

public class PreferencesViewTest {

    SavePreferencesViewModel savePreferencesViewModel = new SavePreferencesViewModel();
    GenerateMealViewModel generateMealViewModel = new GenerateMealViewModel();
    ViewManagerModel viewManagerModel = new ViewManagerModel();
    PreferencesView preferencesView;
    User user = new CommonUserFactory().create("user", "pass");

    @Before
    public void setUp(){
        JFrame app = new JFrame("NutriNinja");
        app.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        CardLayout cardLayout = new CardLayout();
        JPanel views = new JPanel(cardLayout);
        app.add(views);

        FileUserDataAccessObject dao;
        try {
            dao = new FileUserDataAccessObject("test_preferences_view.csv", new CommonUserFactory());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        dao.saveUser(user);

        preferencesView = PreferencesViewFactory.create(viewManagerModel, savePreferencesViewModel, generateMealViewModel, dao);
        views.add(preferencesView, preferencesView.viewName);

        viewManagerModel.setActiveView(preferencesView.viewName);
        viewManagerModel.firePropertyChanged();

        app.pack();
        app.setVisible(true);
    }
    @After
    public void tearDown() {
        File testData = new File("test_preferences_view.csv");
        if (testData.delete()) {
            System.out.println("Deleted test_preferences_view.csv successfully.");
        } else {
            System.out.println("Deleted test_preferences_view.csv unsuccessfully.");
        }
    }

    @Test
    public void testSavePreferencesButton() {
        user.setUserPreferences(new UserPreferences(new NutrientRange(new Range<>(0, 500), new Range<>(0, 500), new Range<>(0, 500), new Range<>(0, 500)), new ArrayList<>(), new ArrayList<>()));
        savePreferencesViewModel.getState().setUsername("user");
        savePreferencesViewModel.getState().getNutrientRange().getCalorieRange().setLowerBound(100);
        savePreferencesViewModel.getState().getNutrientRange().getCalorieRange().setUpperBound(200);
        savePreferencesViewModel.getState().getNutrientRange().getFatRange().setLowerBound(100);
        savePreferencesViewModel.getState().getNutrientRange().getFatRange().setUpperBound(200);
        savePreferencesViewModel.getState().getNutrientRange().getProteinRange().setLowerBound(100);
        savePreferencesViewModel.getState().getNutrientRange().getProteinRange().setUpperBound(200);
        savePreferencesViewModel.getState().getNutrientRange().getCarbRange().setLowerBound(100);
        savePreferencesViewModel.getState().getNutrientRange().getCarbRange().setUpperBound(200);
        savePreferencesViewModel.getState().setHealthPreferences(new ArrayList<>(Arrays.asList("kosher", "gluten-free")));
        savePreferencesViewModel.getState().setDishType(new ArrayList<>(Arrays.asList("salad")));
        savePreferencesViewModel.getState().setMealType(new ArrayList<>(Arrays.asList("lunch")));
        preferencesView.savePreferences.doClick();
        assertEquals("user", savePreferencesViewModel.getState().getUsername());
        assert 100 == savePreferencesViewModel.getState().getNutrientRange().getCalorieRange().getLowerBound();
        assert 200 == savePreferencesViewModel.getState().getNutrientRange().getCalorieRange().getUpperBound();
        assert 100 == savePreferencesViewModel.getState().getNutrientRange().getFatRange().getLowerBound();
        assert 200 == savePreferencesViewModel.getState().getNutrientRange().getFatRange().getUpperBound();
        assert 100 == savePreferencesViewModel.getState().getNutrientRange().getProteinRange().getLowerBound();
        assert 200 == savePreferencesViewModel.getState().getNutrientRange().getProteinRange().getUpperBound();
        assert 100 == savePreferencesViewModel.getState().getNutrientRange().getCarbRange().getLowerBound();
        assert 200 == savePreferencesViewModel.getState().getNutrientRange().getCarbRange().getUpperBound();
        assertEquals("Preferences", viewManagerModel.getActiveView());
    }

    @Test
    public void testGenerateMealButton(){
        user.setUserPreferences(new UserPreferences(new NutrientRange(new Range<>(0, 500), new Range<>(0, 500), new Range<>(0, 500), new Range<>(0, 500)), new ArrayList<>(), new ArrayList<>()));
        savePreferencesViewModel.getState().setUsername("user");
        savePreferencesViewModel.getState().getNutrientRange().getCalorieRange().setLowerBound(0);
        savePreferencesViewModel.getState().getNutrientRange().getCalorieRange().setUpperBound(2000);
        savePreferencesViewModel.getState().getNutrientRange().getFatRange().setLowerBound(0);
        savePreferencesViewModel.getState().getNutrientRange().getFatRange().setUpperBound(200);
        savePreferencesViewModel.getState().getNutrientRange().getProteinRange().setLowerBound(0);
        savePreferencesViewModel.getState().getNutrientRange().getProteinRange().setUpperBound(200);
        savePreferencesViewModel.getState().getNutrientRange().getCarbRange().setLowerBound(0);
        savePreferencesViewModel.getState().getNutrientRange().getCarbRange().setUpperBound(500);
        savePreferencesViewModel.getState().setHealthPreferences(new ArrayList<>(Arrays.asList("kosher", "gluten-free")));
        savePreferencesViewModel.getState().setDishType(new ArrayList<>(Arrays.asList("Salad")));
        savePreferencesViewModel.getState().setMealType(new ArrayList<>(Arrays.asList("Lunch")));
        preferencesView.generateMeal.doClick();
        assertEquals("user", savePreferencesViewModel.getState().getUsername());
        assert 0 == savePreferencesViewModel.getState().getNutrientRange().getCalorieRange().getLowerBound();
        assert 2000 == savePreferencesViewModel.getState().getNutrientRange().getCalorieRange().getUpperBound();
        assert 0 == savePreferencesViewModel.getState().getNutrientRange().getFatRange().getLowerBound();
        assert 200 == savePreferencesViewModel.getState().getNutrientRange().getFatRange().getUpperBound();
        assert 0 == savePreferencesViewModel.getState().getNutrientRange().getProteinRange().getLowerBound();
        assert 200 == savePreferencesViewModel.getState().getNutrientRange().getProteinRange().getUpperBound();
        assert 0 == savePreferencesViewModel.getState().getNutrientRange().getCarbRange().getLowerBound();
        assert 500 == savePreferencesViewModel.getState().getNutrientRange().getCarbRange().getUpperBound();
        assertEquals("Generate Meal", viewManagerModel.getActiveView());
    }
}