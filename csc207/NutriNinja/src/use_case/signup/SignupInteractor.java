
package use_case.signup;

import entity.User;
import entity.UserFactory;

public class SignupInteractor implements SignupInputBoundary {
    final SignupDataAccessInterface userDataAccessObject;
    final SignupOutputBoundary userPresenter;
    final UserFactory userFactory;

    public SignupInteractor(SignupDataAccessInterface signupDataAccessInterface, SignupOutputBoundary signupOutputBoundary, UserFactory userFactory) {
        this.userDataAccessObject = signupDataAccessInterface;
        this.userPresenter = signupOutputBoundary;
        this.userFactory = userFactory;
    }

    public void execute(SignupInputData signupInputData) {
        if (this.userDataAccessObject.userExists(signupInputData.getUsername())) {
            this.userPresenter.prepareFailView("User already exists.");
        } else if (!signupInputData.getPassword().equals(signupInputData.getRepeatPassword())) {
            this.userPresenter.prepareFailView("Passwords don't match.");
        } else {
            // Create user with just the username and password
            User newUser = this.userFactory.create(signupInputData.getUsername(), signupInputData.getPassword());

            // Save the new user using saveUser
            this.userDataAccessObject.saveUser(newUser);

            SignupOutputData signupOutputData = new SignupOutputData(newUser.getUsername());
            this.userPresenter.prepareSuccessView(signupOutputData);
        }
    }
}
