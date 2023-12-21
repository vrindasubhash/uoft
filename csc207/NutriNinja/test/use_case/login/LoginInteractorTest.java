package use_case.login;

import app.custom_data.Range;
import data_access.MemoryUserDataAccessObject;
import entity.CommonUser;
import entity.CommonUserFactory;
import entity.NutrientRange;
import entity.UserPreferences;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.prefs.Preferences;

import static org.junit.Assert.*;

public class LoginInteractorTest {
    MemoryUserDataAccessObject userDataAccessObject;
    String firstUser = "Bob";
    String firstPassword = "pass";

    @Before
    public void setUp() throws Exception {
        this.userDataAccessObject = new MemoryUserDataAccessObject();
        this.userDataAccessObject.saveUser(new CommonUserFactory().create(this.firstUser, this.firstPassword));
    }

    @Test
    public void testUserExistsAndPasswordCorrect() {
        String name = this.firstUser;
        String password = this.firstPassword;

        LoginOutputBoundary loginPresenter = new LoginOutputBoundary() {
            @Override
            public void prepareSuccessView(LoginOutputData user) {
                assertEquals(name, user.getUsername());

                // Testing preferences
                UserPreferences userPreferences = user.getUserPreferences();
                List<String> emptyList = new ArrayList<>();
                assertEquals(emptyList, userPreferences.getHealthPreferences());
                assertEquals(emptyList, userPreferences.getDishType());

                NutrientRange nutrientRange = user.getUserPreferences().getNutrientRange();
                Range<Integer> calRange = nutrientRange.getCalorieRange();
                Range<Integer> fatRange = nutrientRange.getFatRange();
                Range<Integer> proteinRange = nutrientRange.getProteinRange();
                Range<Integer> carbRange = nutrientRange.getCarbRange();
                assertArrayEquals(new int[]{0, 2000}, new int[]{calRange.getLowerBound(), calRange.getUpperBound()});
                assertArrayEquals(new int[]{0, 100}, new int[]{fatRange.getLowerBound(), fatRange.getUpperBound()});
                assertArrayEquals(new int[]{0, 150}, new int[]{proteinRange.getLowerBound(), proteinRange.getUpperBound()});
                assertArrayEquals(new int[]{0, 500}, new int[]{carbRange.getLowerBound(), carbRange.getUpperBound()});
            }

            @Override
            public void prepareFailView(String error) {
                fail("User is in the data access object, but fail view was called.");
            }
        };
        LoginInputData loginInputData = new LoginInputData(name, password);
        LoginInteractor loginInteractor = new LoginInteractor(this.userDataAccessObject, loginPresenter);
        loginInteractor.execute(loginInputData);
    }

    @Test
    public void testWrongPassword() {
        String name = this.firstUser;
        String password = this.firstPassword + "x";
        LoginOutputBoundary loginPresenter = new LoginOutputBoundary() {
            @Override
            public void prepareSuccessView(LoginOutputData user) {
                fail("Succeeded even with the wrong password.");
            }

            @Override
            public void prepareFailView(String error) {
                String expectedMessage = "Incorrect password for " + name + ".";
                assertEquals(expectedMessage, error);
            }
        };
        LoginInputData loginInputData = new LoginInputData(name, password);
        LoginInteractor loginInteractor = new LoginInteractor(this.userDataAccessObject, loginPresenter);
        loginInteractor.execute(loginInputData);
    }

    @Test
    public void testUserDoesNotExist() {
        String name = this.firstUser + "1";
        String password = this.firstPassword;
        LoginOutputBoundary loginPresenter = new LoginOutputBoundary() {
            @Override
            public void prepareSuccessView(LoginOutputData user) {
                fail("User is not in the data access object, but success view was called.");
            }

            @Override
            public void prepareFailView(String error) {
                String expectedMessage = name + ": Account does not exist.";
                assertEquals(expectedMessage, error);
            }
        };
        LoginInputData loginInputData = new LoginInputData(name, password);
        LoginInteractor loginInteractor = new LoginInteractor(this.userDataAccessObject, loginPresenter);
        loginInteractor.execute(loginInputData);
    }
}