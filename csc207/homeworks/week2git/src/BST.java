/**
 * A minimal implementation of a binary search tree. See the python version for
 * additional documentation.
 *
 * You can also see Chapter 6 of <a href="https://www.teach.cs.toronto.edu/~csc148h/winter/notes/">CSC148 Course Notes</a>
 * if you want a refresher on BSTs, but it is required to complete this assignment.
 * @param <T>
 */
public class BST<T extends Comparable<T>> {
    //Note: the extends Comparable<T> above means we require T to implement the Comparable<T> interface,
    //      since a BST requires that we can compare its elements to determine the ordering.
    private T root;

    private BST<T> left;
    private BST<T> right;

    public BST(T root) {
        if (root != null) { // check to ensure we don't accidentally try to store null at the root!
            this.root = root;
            this.left = new BST<>();
            this.right = new BST<>();
        }
        // Note: each of the attributes will default to null
    }

    /**
     * Alternate constructor, so we don't have to explicitly pass in null.
     */
    public BST() {
        this(null);
    }



    public boolean isEmpty() {
        return this.root == null;
    }

    public boolean contains(T item) {
        // provided
        if (this.isEmpty()) {
            return false;
        } else if (item.equals(this.root)) { // we need to use .equals and not == to properly compare values
            return true;
        } else if (item.compareTo(this.root) < 0) {
            return this.left.contains(item);
        }
        return this.right.contains(item);
    }


    public void insert(T item) {
        if (this.isEmpty()) {
            this.root = item;
            this.left = new BST<>();
            this.right = new BST<>();
        }
        else if (item.compareTo(this.root) <= 0) {
            this.left.insert(item);
        }
        else {
            this.right.insert(item);
        }
    }


    public void delete(T item) {
        if (this.isEmpty()) {
            return;
        } else if (this.root.equals(item)) {
            this.deleteRoot();
        } else if (item.compareTo(this.root) < 0) {
            this.left.delete(item);
        } else {
            this.right.delete(item);
        }
    }

    private void deleteRoot() {
        if (this.left.isEmpty() && this.right.isEmpty()) {
            this.root = null;
        } else if (this.left.isEmpty()) {
            T tmpRoot = this.right.root;
            BST<T> tmpLeft = this.right.left;
            BST<T> tmpRight = this.right.right;

            this.root = tmpRoot;
            this.left = tmpLeft;
            this.right = tmpRight;

        } else if (this.right.isEmpty()) {
            T tmpRoot = this.left.root;
            BST<T> tmpLeft = this.left.left;
            BST<T> tmpRight = this.left.right;

            this.root = tmpRoot;
            this.left = tmpLeft;
            this.right = tmpRight;
        } else {
            this.root = this.left.extractMax();
        }
    }


    private T extractMax() {
        if (this.right.isEmpty()) {
            T maxItem = this.root;

            T tmpRoot = this.left.root;
            BST<T> tmpLeft = this.left.left;
            BST<T> tmpRight = this.left.right;

            this.root = tmpRoot;
            this.left = tmpLeft;
            this.right = tmpRight;
            return maxItem;
        } else {
            return this.right.extractMax();
        }
    }

    public int height() {
        if (this.isEmpty()) {
            return 0;
        } else {
            return Math.max(this.left.height(), this.right.height()) + 1;
        }
    }

    public int count(T item) {
        if (this.isEmpty()) {
            return 0;
        } else if (this.root.compareTo(item) > 0) {
            return this.left.count(item);
        } else if (this.root.equals(item)) {
            return 1 + this.left.count(item) + this.right.count(item);
        } else {
            return this.right.count(item);
        }
    }


    public int getLength() {
        if (this.isEmpty()) {
            return 0;
        } else {
            return 1 + this.left.getLength() + this.right.getLength();
        }
    }

    public static void main(String[] args) {
        BST<Integer> bst = new BST<>();
        bst.insert(5);
        bst.insert(3);
        bst.insert(7);
        bst.insert(2);
        bst.insert(4);
        bst.insert(6);
        bst.insert(8);
        bst.insert(4);  // duplicates
        bst.insert(4);

        System.out.println(bst.contains(5));
        System.out.println(bst.contains(1));
        System.out.println(bst.contains(4));

        // Count occurrences of values.
        System.out.println(bst.count(4));
        System.out.println(bst.count(7));
        System.out.println(bst.count(9));

        System.out.println(bst.height());

        bst.delete(5);
        System.out.println(bst.contains(5));

        System.out.println(bst.getLength());
    }

}
