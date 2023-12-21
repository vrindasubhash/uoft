package use_case.login;

import entity.User;

public interface LoginUserDataAccessInterface {
    boolean userExists(String identifier);

    User getUser(String username);
}
