
package use_case.signup;

public interface SignupOutputBoundary {
    void prepareSuccessView(SignupOutputData successResponse);

    void prepareFailView(String failureResponse);
}
