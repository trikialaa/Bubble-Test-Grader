# Bubble Test Grader

Implementation of image processing techniques to detect the elements of a bubble test and correct it according to pre-defined answers

## Dependencies

This project uses the following dependencies:
* Numpy
* OpenCV
* Imutils

## Usage

1- Customize the document "template.docx" without moving the bubbles positions

2- Print the test document and fill it with your answers then scan it into "template.jpg"

3- Insert your ordered answers in the document "answers.txt"

```java
// Line N represents the answer to question N
A // Answer for question 1 is A
B // Answer for question 2 is B
BC // Answer for question 3 is B and C
CD // Answer for question 4 is C and D
```

4- Run the python code main.py

```bash
python main.py
```

5- The result will show the inscription number and the score, and will output an result picture at "out.png"

![Output Graded Test](out.png)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
