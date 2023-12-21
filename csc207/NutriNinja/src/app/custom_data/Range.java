package app.custom_data;

public class Range <T extends Number> {
    private T lowerBound;
    private T upperBound;

    public Range(T lowerBound, T upperBound) {
        this.lowerBound = lowerBound;
        this.upperBound = upperBound;
    }

    public T getLowerBound() {
        return lowerBound;
    }

    public void setLowerBound(T lowerBound) {
        this.lowerBound = lowerBound;
    }

    public T getUpperBound() {
        return upperBound;
    }

    public void setUpperBound(T upperBound) {
        this.upperBound = upperBound;
    }

    // Ranges are inclusive of both bounds.
    public String getRangeString(){
        return lowerBound + "-" + upperBound;
    }
}
