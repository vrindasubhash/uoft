import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;

/**
 * This is the provided NumberTriangle class to be used in this assignment.
 *
 * Note: This is like a tree, but some nodes in the structure have two parents.
 *
 * The structure is shown below. Observe that the parents of e are b and c, whereas
 * d and f each only have one parent. Each row is complete and will never be missing
 * a node. So each row has one more NumberTriangle object than the row above it.
 *
 *                  a
 *                b   c
 *              d   e   f
 *            h   i   j   k
 *
 * Also note that this data structure is minimally defined and is only intended to
 * be constructed using the Problem18.loadTriangle method, which you will implement
 * in Problem18.java. We have not included any code to enforce the structure noted above,
 * and you don't have to write any either.
 *
 *
 * See Problem18Test.java for a few basic test cases.
 *
 * Extra: If you decide to solve the Project Euler problems (see Problem18.java),
 *        feel free to add extra methods to this class. Just make sure that your
 *        code still compiles and runs so that we can run our tests.
 *
 */
public class NumberTriangle {

    private final int root;

    private NumberTriangle left;
    private NumberTriangle right;

    public NumberTriangle(int root) {
        this.root = root;
    }

    public void setLeft(NumberTriangle left) {
        this.left = left;
    }


    public void setRight(NumberTriangle right) {
        this.right = right;
    }

    public int getRoot() {
        return root;
    }


    public boolean isLeaf() {
        return right == null && left == null;
    }

    public static void main(String[] args) {
        // you can put any code that you want here as you write the code; we will not
        // run this method.
        NumberTriangle root = new NumberTriangle(5);
        NumberTriangle left = new NumberTriangle(7);
        NumberTriangle right = new NumberTriangle(2);
        NumberTriangle rr = new NumberTriangle(1);
        NumberTriangle ll = new NumberTriangle(9);
        NumberTriangle lr = new NumberTriangle(8);
        NumberTriangle rl = new NumberTriangle(4);

        root.setLeft(left);
        root.setRight(right);

        left.setLeft(ll);
        left.setRight(lr);
        right.setRight(rr);
        right.setLeft(rl);

        System.out.println(root.root);
        String[] paths = {"", "l", "r", "lr"};
        System.out.println("trying each path...");
        for (String path :
                paths) {
            System.out.println(path + " = " + root.retrieve(path));
        }
    }


    /**
     * Follows path through this NumberTriangle structure ('l' = left; 'r' = right) and
     * returns the root value at the end of the path. An empty string will return
     * the root of the NumberTriangle.
     *
     * You can decide if you want to use a recursive or an iterative approach in your solution.
     *
     * You can assume that:
     *      the length of path is less than the height of this NumberTriangle structure.
     *      the NumberTriangle structure is not empty.
     *
     * @param path the path through this NumberTriangle to follow
     * @return the root value at the location indicated by path
     * @throws RuntimeException If a char in the path is neither 'l' nor 'r', a RuntimeException should be thrown.
     *
     */

    public int retrieve(String path) {
        NumberTriangle current = this;

        for (int i = 0; i < path.length(); i++) {
            if (path.charAt(i) == 'l') {
                current = current.left;
            }
            else {
                if (path.charAt(i) == 'r') {
                    current = current.right;
                }
                else {
                    throw new RuntimeException("Char in path is not valid.");
                }
            }
            if (current == null) {
                throw new RuntimeException("The path cannot be followed (missing child).");
            }
        }

        return current.getRoot();
    }



    public int retrieveRecursive(String path) {

        if (path.isEmpty()) {
            return this.getRoot();
        }

        NumberTriangle current;

        if (path.charAt(0) == 'l') {
            current = this.left;
        }
        else {
            if (path.charAt(0) == 'r') {
                current = this.right;
            }
            else {
                throw new RuntimeException("Char in path is not valid.");
            }
        }
        if (current == null) {
            throw new RuntimeException("The path cannot be followed (missing child).");
        }

        return current.retrieveRecursive(path.substring(1));
    }


    public void printTree() {
        Queue<NumberTriangle> current = new LinkedList<>();
        Queue<NumberTriangle> next = new LinkedList<>();

        current.offer(this);

        while (!current.isEmpty()) {
            NumberTriangle item = current.poll();
            System.out.print(item.getRoot() + " ");
            if (item.left != null) {
                next.offer(item.left);
                if (current.isEmpty()) {
                    next.offer(item.right);
                }
            }
            if (current.isEmpty()) {
                System.out.println();
                current = next;
                next = new LinkedList<>();
            }
        }
    }
}
