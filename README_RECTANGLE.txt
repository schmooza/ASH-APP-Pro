NEW BUILT-IN RECTANGLE FUNCTION

In student_images.py, import rectangle_shape from teacher_sequence.

Example:
rectangle = Pattern("Rectangle").at(-2, -1).shape(rectangle_shape(4, 2)).draw()

Then include ("Rectangle", rectangle) in image_sequence.

rectangle_shape(width, height) takes positive whole-number dimensions in grid units.
The default is rectangle_shape(4, 2). The function uses the existing forward/turn/repeat commands.
The example in student_images.py is included but commented out in image_sequence; remove the # to display it.
