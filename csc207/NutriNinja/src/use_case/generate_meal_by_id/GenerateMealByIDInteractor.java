package use_case.generate_meal_by_id;

import com.google.gson.Gson;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.ResponseBody;

import java.io.IOException;

public class GenerateMealByIDInteractor implements GenerateMealByIDInputBoundary {
    final GenerateMealByIDOutputBoundary generateMealByIDPresenter;

    public GenerateMealByIDInteractor(GenerateMealByIDOutputBoundary generateMealByIDPresenter) {
        this.generateMealByIDPresenter = generateMealByIDPresenter;
    }

    /**
     * This method calls the API and gets the data from the API, and calls the outputBoundary to prepare the view
     * @param inputData: the input data obtained from the user.
     */
    @Override
    public void execute(GenerateMealByIDInputData inputData) {
        String ID = "8da598eb";
        String KEY = " 9fec3b1b7ba00da5dac76ba4af6bd26e\t";
        String URL = "https://api.edamam.com/api/recipes/v2/" + inputData.getMealID() + "?type=public&app_id=" + ID + "&app_key=" + KEY;

        OkHttpClient client = new OkHttpClient().newBuilder().build();

        Request request = new Request.Builder()
                .url(URL)
                .addHeader("Accept", "application/json")
                .addHeader("Accept-Language", "en")
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (response.code() == 200) {
                Gson responseBody = new Gson();
                ResponseBody body = response.body();
                String content = body.string(); // Needed to be called only once, or else responseBody.fromJson will not work
                GenerateMealByIDOutputData outputData = responseBody.fromJson(content, GenerateMealByIDOutputData.class);
                generateMealByIDPresenter.prepareSuccessView(outputData);
            } else {
                generateMealByIDPresenter.prepareFailView("Error (Code " + response.code() + ").");
            }
        } catch (IOException e) {
            generateMealByIDPresenter.prepareFailView(e.getMessage());
        }
    }
}
