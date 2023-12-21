package use_case.login;

import entity.UserPreferences;

public class LoginOutputData {

    private final String username;
    private final UserPreferences userPreferences;

    public LoginOutputData(String username, UserPreferences userPreferences) {
        this.username = username;
        this.userPreferences = userPreferences;
    }

    public String getUsername() {
        return this.username;
    }

    public UserPreferences getUserPreferences() {
        return this.userPreferences;
    }
}
