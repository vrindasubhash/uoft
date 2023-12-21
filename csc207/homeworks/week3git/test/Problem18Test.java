import org.junit.Test;

import java.io.IOException;

import static org.junit.Assert.*;

public class Problem18Test {

    // this is testing that aliasing exists between
    // mt.left.right and mt.right.left
    @Test
    public void aliasingTree() throws IOException {

        NumberTriangle mt = Problem18.loadTriangle("input_tree.txt");
        assertEquals(mt.retrieve("lr"), mt.retrieve("lr"));
    }

    @Test
    public void rootTree() throws IOException {

        NumberTriangle mt = Problem18.loadTriangle("input_tree.txt");
        assertEquals(75, mt.retrieve(""));
    }

    @Test
    public void retrieveTree() throws IOException {

        NumberTriangle mt = Problem18.loadTriangle("input_tree.txt");
        assertEquals(47, mt.retrieve("lr"));
    }

    // this syntax ensures that the method is properly throwing
    // a RuntimeException
    @Test(expected = RuntimeException.class)
    public void retrieveTreeFailure() throws IOException {

        NumberTriangle mt = Problem18.loadTriangle("input_tree.txt");
        mt.retrieve("sr");
    }

    @Test
    public void littleTree() throws IOException {

        NumberTriangle mt = Problem18.loadTriangle("little_tree.txt");
        assertEquals(1, mt.retrieve(""));
        assertEquals(2, mt.retrieve("l"));
        assertEquals(3, mt.retrieve("r"));
    }
}