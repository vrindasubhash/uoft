package entity;

public class CommonUser implements User {
    private String username;
    private String password;
    private UserPreferences userPreferences;

    public CommonUser(String username, String password, UserPreferences userPreferences) {
        this.username = username;
        this.password = password;
        this.userPreferences = userPreferences;
    }

    @Override
    public String getUsername() {
        return username;
    }

    @Override
    public String getPassword() {
        return password;
    }

    @Override
    public UserPreferences getUserPreferences() {
        return userPreferences;
    }

    @Override
    public void setUsername(String username) {
        this.username = username;
    }

    @Override
    public void setPassword(String password) {
        this.password = password;
    }

    @Override
    public void setUserPreferences(UserPreferences userPreferences) {
        this.userPreferences = userPreferences;
    }
}
