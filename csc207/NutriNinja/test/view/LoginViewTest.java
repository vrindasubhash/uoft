package view;

import app.LoginViewFactory;
import data_access.FileUserDataAccessObject;
import entity.CommonUserFactory;
import entity.NutrientRange;
import entity.User;
import entity.UserPreferences;
import interface_adapter.ViewManagerModel;
import interface_adapter.login.LoginViewModel;
import interface_adapter.save_preferences.SavePreferencesState;
import interface_adapter.save_preferences.SavePreferencesViewModel;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import static org.junit.Assert.*;

public class LoginViewTest {
    LoginViewModel loginViewModel = new LoginViewModel();
    SavePreferencesViewModel savePreferencesViewModel = new SavePreferencesViewModel();
    ViewManagerModel viewManagerModel = new ViewManagerModel();
    User user = new CommonUserFactory().create("test_user", "test_password");
    LoginView loginView;

    @Before
    public void setUp() throws Exception {
        JFrame app = new JFrame("NutriNinja");
        app.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        CardLayout cardLayout = new CardLayout();
        JPanel views = new JPanel(cardLayout);
        app.add(views);

        // Setting up view manager and models
        new ViewManager(views, cardLayout, viewManagerModel);

        // Initiating data access object
        FileUserDataAccessObject dao;
        try {
            dao = new FileUserDataAccessObject("test_login_view.csv", new CommonUserFactory());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        dao.saveUser(user);

        // Creating LoginView
        loginView = LoginViewFactory.create(viewManagerModel, loginViewModel, savePreferencesViewModel, dao);
        views.add(loginView, loginView.viewName);

        viewManagerModel.setActiveView(loginViewModel.getViewName());
        viewManagerModel.firePropertyChanged();

        app.pack();
        app.setVisible(true);
    }

    @After
    public void tearDown() {
        File testData = new File("test_login_view.csv");
        if (testData.delete()) {
            System.out.println("Deleted test_login_view.csv successfully.");
        } else {
            System.out.println("Deleted test_login_view.csv unsuccessfully.");
        }
    }

    @Test
    public void testLoginSuccess() {
        loginView.usernameInputField.setText("test_user");
        loginView.passwordInputField.setText("test_password");
        loginView.logIn.doClick();

        UserPreferences userPreferences = user.getUserPreferences();
        NutrientRange nutrientRange = userPreferences.getNutrientRange();
        SavePreferencesState state = savePreferencesViewModel.getState();
        assertEquals(userPreferences.getHealthPreferences(), state.getHealthPreferences());
        assertEquals(userPreferences.getDishType(), state.getDishType());
        assertEquals(new ArrayList<>(), state.getMealType());

        assertEquals("0-2000", nutrientRange.getCalorieRange().getRangeString());
        assertEquals("0-100", nutrientRange.getFatRange().getRangeString());
        assertEquals("0-150", nutrientRange.getProteinRange().getRangeString());
        assertEquals("0-500", nutrientRange.getCarbRange().getRangeString());
        assertEquals("Preferences", viewManagerModel.getActiveView());
    }

    @Test
    public void testLoginIncorrectPassword() {
        loginView.usernameInputField.setText("test_user");
        loginView.passwordInputField.setText("test_password1");
        loginView.logIn.doClick();

        assertEquals("Incorrect password for test_user.", loginView.errorField.getText());
        assertEquals("Login", viewManagerModel.getActiveView());
    }

    @Test
    public void testLoginIncorrectUsernameOrPassword() {
        loginView.usernameInputField.setText("nonexistent_user");
        loginView.passwordInputField.setText("nonexistent_password");
        loginView.logIn.doClick();

        assertEquals("nonexistent_user: Account does not exist.", loginView.errorField.getText());
        assertEquals("Login", viewManagerModel.getActiveView());
    }
}