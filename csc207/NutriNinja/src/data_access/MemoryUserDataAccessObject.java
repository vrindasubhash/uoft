package data_access;

import entity.User;
import entity.UserPreferences;
import use_case.login.LoginUserDataAccessInterface;
import use_case.save_preferences.SavePreferencesDataAccessInterface;
import use_case.signup.SignupDataAccessInterface;

import java.util.HashMap;
import java.util.Map;

public class MemoryUserDataAccessObject implements LoginUserDataAccessInterface,
        SignupDataAccessInterface,
        SavePreferencesDataAccessInterface {
    private final Map<String, User> accounts = new HashMap<>();

    /**
     * Saves user to database
     * @param user represents the user to save
     */
    @Override
    public void saveUser(User user) {
        accounts.put(user.getUsername(), user);
    }

    /**
     * Saves user preferences to database
     * @param username represents the username of the user to save to
     * @param preferences represents the new preferences
     */
    @Override
    public void saveUserPreferences(String username, UserPreferences preferences) {
        User user = accounts.get(username);
        user.setUserPreferences(preferences);
    }

    /**
     * Returns true if the user exists and false otherwise
     * @param username identifies the user you want to check exists
     * @return a boolean representing if the user exists or not
     */
    @Override
    public boolean userExists(String username) {
        return accounts.containsKey(username);
    }

    /**
     * Returns a user object representing the user
     * @param username identifies the user
     * @return the user
     */
    @Override
    public User getUser(String username) {
        return accounts.get(username);
    }
}
