# LPATH tells the linker where to find libraries
LPATH = -L/usr/openwin/lib -L/home/cs433/Fall00/Mesa-3.2.1/lib

# IPATH tells the compiler where to look for include files.
IPATH = -I/home/cs433/Fall00/Mesa-3.2.1/include

# GLLIBS are the GLUT and OpenGL (or Mesa) libraries needed by the linker.
GLLIBS = -lglut -lGLU -lGL

# XLIBS are the X libraries needed by the linker because GLUT and OpenGL
#       call X routines.
XLIBS = -lXi -lXmu -lX11 -lXext

# MISCLIBS are miscellaneous libs that are needed by the linker.
# -lm denotes the math library.
MISCLIBS = -lm

LIBS = $(LPATH) $(GLLIBS) $(XLIBS) $(MISCLIBS)

# compiler
CC = gcc
# compiler flags:
# -g	tells the compiler to produce symbolic information that a debugger
#	(like gdb) needs.
# -Wall	tells the compiler to print warnings about pretty much everything.
CFLAGS = -g -Wall


bresenham: bresenham.o
	$(CC) $(CFLAGS) -o bresenham bresenham.o $(LIBS)


# The default way to convert .c files into .o files.
.cpp.o:		; $(CC) -c $(CFLAGS) $(IPATH) $<


clean:
	$(RM) *.o bresenham 
