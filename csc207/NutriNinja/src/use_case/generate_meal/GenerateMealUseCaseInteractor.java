package use_case.generate_meal;

import com.google.gson.Gson;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.ResponseBody;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

public class GenerateMealUseCaseInteractor implements GenerateMealInputBoundary{

    final GenerateMealOutputBoundary generateMealPresenter;

    public GenerateMealUseCaseInteractor (GenerateMealOutputBoundary generateMealsOutputBoundary){
        this.generateMealPresenter = generateMealsOutputBoundary;

    }

    /**
     * This method calls the API and gets the data from the API, and calls the outputBoundary to prepare the view
     * @param inputData: the input data obtained from the user.
     */
    public void execute(GenerateMealInputData inputData) {
        String ID = "8da598eb";
        String KEY = " 9fec3b1b7ba00da5dac76ba4af6bd26e\t";
        String URL = "https://api.edamam.com/api/recipes/v2?type=public&app_id=" + ID + "&app_key=" + KEY;
        String imageSizeURL = "&imageSize=REGULAR";

        //fields to specify the data we want to get from the API
        List<String> fields = Arrays.asList("label", "image", "source", "url", "ingredientLines",
                "calories", "totalTime", "totalNutrients", "yield", "healthLabels", "mealType", "dishType");


        String healthPreferencesURL = convertArrtoStringURL("&health=", inputData.getHealthPreferences());
        String mealTypeURL = convertArrtoStringURL("&mealType=", inputData.getMealType());
        String dishTypeURL = convertArrtoStringURL("&dishType=", inputData.getDishType());
        String calRangeURL = "&calories=" + inputData.getCalRange();
        String carbRangeURL = "&nutrients%5BCHOCDF.net%5D=" + inputData.getCarbRange(); //Carbs
        String proteinRangeURL = "&nutrients%5BPROCNT%5D=" + inputData.getProteinRange(); //Protein
        String fatRangeURL = "&nutrients%5BFAT%5D=" + inputData.getFatRange(); //Fat
        String field = convertArrtoStringURL("&field=", fields);
        String random = "&random=true";

        OkHttpClient client = new OkHttpClient().newBuilder()
                .build();

        Request request = new Request.Builder()
                .url(String.format("%s%s%s%s%s%s%s%s%s%s%s", URL, imageSizeURL, healthPreferencesURL, mealTypeURL,
                        dishTypeURL, calRangeURL, carbRangeURL, proteinRangeURL, fatRangeURL, field, random))
                .addHeader("Accept", "application/json")
                .addHeader("Accept-Language", "en")
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (response.code() == 200) {
                Gson responseBody = new Gson();
                ResponseBody body = response.body();
                String content = body.string(); // Needed to be called only once, or else responseBody.fromJson will not work
                GenerateMealOutputData outputData = responseBody.fromJson(content, GenerateMealOutputData.class);

                //No meals found
                if (outputData.getMeals().length == 0)
                    generateMealPresenter.prepareFailView("No meals found, please try again.");
                else
                    generateMealPresenter.prepareSuccessView(outputData);


            } else {

                generateMealPresenter.prepareFailView("Error (Code " + response.code() + ").");
            }
        } catch (IOException e) {
            generateMealPresenter.prepareFailView(e.getMessage());
        }
    }


    private String convertArrtoStringURL(String urlName, List<String> arr){
        String result = "";
        for (String s : arr){
            result += urlName + s;
        }
        return result;
    }

}
