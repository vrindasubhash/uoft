import javax.sound.midi.Soundbank;
import java.io.*;
import java.util.*;

/**
 * This is the basic setup for loading data to then attempt to solve Problem 18 (and 67)
 * from Project Euler (https://projecteuler.net/problem=18)
 *
 *
 * Extra: Solve problems 18 and 67 [not for credit]
 *
 */
public class Problem18 {

    public static void main(String[] args) {

        try {
//            NumberTriangle mt = loadTriangle("little_tree.txt");
            NumberTriangle mt = loadTriangle("input_tree.txt");
//            mt.printTree();

            // you can add code here if you want to try to solve
            // Problem 18 from project Euler [not for credit]

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        // and you can also try Problem 67 [not for credit]
    }

    /** Reads in the NumberTriangle structure from a file.
     *
     * You may assume that it is a valid format with a height of at least 1,
     * so there is at least one line with a number on it to start the file.
     *
     * See input_tree.txt for an example NumberTriangle format.
     *
     * The first row is the root of the NumberTriangle (call it 0).
     * The second line contains the two children of the root (call them 1L and 1R).
     * The third line contains the three numbers corresponding to:
     *      - the left child of 1L, call it (2LL)
     *      - the right child of 1L, call it (2LR)
     *      - the left child of 1R, call it (2RL)
     *      - the right child of 1R, call it (2RR)
     *   NOTE: 2RL and 2LR will correspond to the same underlying NumberTriangle object.
     *
     *   Hint 0: Start by making a plan and scaffolding what you plan to do; if you
     *           are still finding it hard to "think in Java", write some comments describing
     *           what you want to do or try implementing some of the logic in Python.
     *
     *   Hint 1: Base your file reading code off what was shown in lecture last
     *           week for reading a csv file line by line and splitting strings.
     *
     *   Hint 2: Think about what you need to keep track of on each iteration of the loop and
     *           make appropriate variables to store those things.
     *
     *   Hint 3: Related to 2, think about how to connect NumberTriangle objects between layers in the
     *           structure.
     *
     *   Hint 4: If you are still stuck, it might help to think of a sub problem you can solve,
     *           then design the logic of your solution around that helper, which you can
     *           implement separately. This kind of decomposition of a problem can make it much
     *           more manageable.
     *
     * @param fname the file to load the NumberTriangle structure from
     * @return the topmost NumberTriangle object in the NumberTriangle structure read from the specified file
     * @throws IOException may occur if an issue reading the file occurs
     */
    public static NumberTriangle loadTriangle(String fname) throws IOException {
        //File f = new File(fname);
        //List<List<Integer>> ll = parseFile("week3git/" + fname);
        List<List<Integer>> ll = parseFile(fname);
        NumberTriangle first = null;

        List<NumberTriangle> lastRow = null;
        for (int i = 0; i < ll.size(); i++) {
            List<NumberTriangle> ln = new ArrayList<>();
            List<Integer> l = ll.get(i);
            for (int j = 0; j < l.size(); j++) {
                NumberTriangle nt = new NumberTriangle(l.get(j));
                if (first == null) {
                    first = nt;
                }
                ln.add(nt);
                if (lastRow != null) {
                    // set the last rows left and right children.
                    if (lastRow.size() > j) {
                        NumberTriangle p1 = lastRow.get(j);
                        p1.setLeft(nt);
                    }
                    if (j-1 >= 0) {
                        NumberTriangle p2 = lastRow.get(j-1);
                        p2.setRight(nt);
                    }
                }
            }
            lastRow = ln;
        }
        return first;
    }

    private static List<List<Integer>> parseFile(String fname) throws IOException {
        List<List<Integer>> ll = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new FileReader(fname));
        try {
            String line;
            while ((line = reader.readLine()) != null) {
                // Split the line based on spaces
                String[] numberStrings = line.split(" ");

                // Convert the number strings to integers and add them to a list
                List<Integer> numbers = new ArrayList<>();
                for (String numberString : numberStrings) {
                    numbers.add(Integer.parseInt(numberString));
                }
                ll.add(numbers);
            }
        } finally {
            reader.close();
        }
        return ll;
    }




}
