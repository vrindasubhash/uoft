package interface_adapter.generate_meal;

import com.google.gson.internal.bind.util.ISO8601Utils;
import interface_adapter.ViewModel;

import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;

public class GenerateMealViewModel extends ViewModel {

    public static final String TITLE = "Meal Page";//TITLE


    //HEADERS
    public static final String MEAL_HEADER = "Meal Suggested: ";

    public static final String SERVINGS_HEADER = "Servings: ";
    public static final String CALORIES_HEADER = "Calories: ";
    public static final String PROTEIN_HEADER = "Protein: ";
    public static final String CARBS_HEADER = "Carbs: ";
    public static final String FAT_HEADER = "Fat: ";
    public final static String INGREDIENTS_HEADER = "Ingredients: ";
    public final static String RECIPE_LINK_HEADER = "Recipe Link: ";
    public final static String RECIPE_SOURCE_HEADER = "Recipe Source:";






    //Buttons
    public final static String BACK_BUTTON_LABEL = "Back";
    public final static String REGENERATE_BUTTON_LABEL = "Generate Another Meal";
    public final static String FEELING_LUCKY_BUTTON_LABEL = "I'm Feeling Lucky";

    private GenerateMealState state= new GenerateMealState();


    public GenerateMealState getState(){
        return state;
    }
    public void setState(GenerateMealState state){
        this.state = state;
    }


    private final PropertyChangeSupport support = new PropertyChangeSupport(this);

    public GenerateMealViewModel() {
        super("Generate Meal");
    }

    @Override
    public void firePropertyChanged() {
        support.firePropertyChange("state", null, this.state);
    }

    @Override
    public void addPropertyChangeListener(PropertyChangeListener listener) {
        support.addPropertyChangeListener(listener);
    }
}
