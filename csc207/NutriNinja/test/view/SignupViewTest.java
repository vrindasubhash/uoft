package view;

import app.SignupViewFactory;
import data_access.FileUserDataAccessObject;
import entity.CommonUserFactory;
import interface_adapter.ViewManagerModel;
import interface_adapter.login.LoginViewModel;
import interface_adapter.signup.SignupViewModel;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import javax.swing.*;

import java.awt.*;
import java.io.File;
import java.io.IOException;

import static org.junit.Assert.*;

public class SignupViewTest {
    SignupViewModel signupViewModel = new SignupViewModel();
    LoginViewModel loginViewModel = new LoginViewModel();
    ViewManagerModel viewManagerModel = new ViewManagerModel();
    SignupView signupView;

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
            dao = new FileUserDataAccessObject("test_signup_view.csv", new CommonUserFactory());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        // Creating SignupView
        signupView = SignupViewFactory.create(viewManagerModel, loginViewModel, signupViewModel, dao);
        views.add(signupView, signupView.viewName);

        viewManagerModel.setActiveView(signupView.viewName);
        viewManagerModel.firePropertyChanged();

        app.pack();
        app.setVisible(true);
    }

    @After
    public void tearDown() {
        File testData = new File("test_signup_view.csv");
        if (testData.delete()) {
            System.out.println("Deleted test_signup_view.csv successfully.");
        } else {
            System.out.println("Deleted test_signup_view.csv unsuccessfully.");
        }
    }

    @Test
    public void testSignupSuccess() {
        signupViewModel.getState().setUsername("test_user");
        signupViewModel.getState().setPassword("test_password");
        signupViewModel.getState().setRepeatPassword("test_password");
        signupView.signUp.doClick();

        assertEquals("test_user", loginViewModel.getState().getUsername());
        assertEquals("Login", viewManagerModel.getActiveView());
    }
}