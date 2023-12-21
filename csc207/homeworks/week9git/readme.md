This assignment is based on the Encryption example from Chapter 19: Policy and Level of the
Clean Architecture textbook. You don't need to read it, but it may help you if you are having trouble
getting started.

Your goal is to write additional code such that `SolutionMain.java` runs successfully and reveals the
encrypted message hidden in `message.txt`.

# Requirements

You must **NOT** modify any of the provided starter code.

You must **NOT** create any new interfaces or abstract classes, as this could interfere with our testing.

You should only create new classes required for `SolutionMain.java` to run.

# Getting Started
* Make sure to mark `src` as the sources root.

* To ensure that `message.txt` can be found when you eventually get to running
  `SolutionMain.java`, we recommend you directly open `week9git` as your IntelliJ
  project. You can alternatively adjust the settings in the run configuration to
  change the "Working directory" as needed.

The `main` method of `StarterMain.java` runs a simple program which reads from the terminal and encrypts
the input using a Caesar cipher, which is a shift cipher (see `StarterMain.encrypt` for additional information).

This basic functionality is nice, but as discussed in the textbook, the program
leaves a lot to be desired in terms of its overall design.

Before you get into writing any code, take a few minutes to consider the provided code and identify
potential places where some of the design patterns discussed in lectures might be applied. You should be
able to spot at least two or three specific patterns — and possibly several places to apply them.

Once you have thought about potential design patterns, take a look at the rest of the provided code. You
should hopefully find that many of the classes and interfaces we have provided align well with the ideas
you came up with!

# Your Task
- [ ] Making use of the provided starter code,
  apply appropriate design patterns as you get `SolutionMain.java` working. You
  will need to write some classes to do so. You should find that most, if not all,
  of the main logic is already implemented in the provided code, so there won't
  be much code to write in the body of any given method. Instead, you will need to
  figure out what classes to define and how to make use of the provided code.

As noted in the requirements, you must NOT change any of the provided code.
**You can only add new classes.**

**Tip: remember that git is tracking your files, so if you accidentally edit a starter file, the status of
  that file will indicate that it has been modified. You can also make sure not to commit any changes to the
  starter files; only commit the new files you write.**

- [ ] For one of the places where you applied a design pattern,
write a short paragraph indicating which design pattern you applied.
This can be very short; we just want you to convince us you chose and applied an appropriate pattern.

Include a UML class diagram showing the relevant classes involved.

# What to hand in

- push a file called `design-pattern.pdf` containing the diagram and paragraph about
  one of the design patterns you applied.
- push the Java files for any classes that you wrote.

And that's it. Great job, you did it!
