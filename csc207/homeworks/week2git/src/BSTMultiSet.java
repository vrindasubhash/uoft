public class BSTMultiSet<T extends Comparable<T>> implements MultiSet<T>{

    // a multiset always starts empty, so we can directly instantiate our private attribute
    // here; no need to explicitly write a new constructor.
    private final BST<T> bst = new BST<>();

    @Override
    public void add(T item) {
        this.bst.insert(item);
    }

    @Override
    public void remove(T item) {
        this.bst.delete(item);
    }

    @Override
    public boolean contains(T item) {
        return this.bst.contains(item);
    }

    @Override
    public boolean isEmpty() {
        return this.bst.isEmpty();
    }

    @Override
    public int count(T item) {
        return this.bst.count(item);
    }

    @Override
    public int size() {
        return this.bst.getLength();
    }

}
