package entity;

public interface User {
    String getUsername();
    String getPassword();
    UserPreferences getUserPreferences();

    void setUsername(String username);
    void setPassword(String password);
    void setUserPreferences(UserPreferences preferences);
}
