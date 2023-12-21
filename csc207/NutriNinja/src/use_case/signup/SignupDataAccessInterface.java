

package use_case.signup;

import entity.User;

public interface SignupDataAccessInterface {
    boolean userExists(String username);

    public void saveUser(User user);
}
