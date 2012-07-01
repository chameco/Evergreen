evergreen : main.o
	g++ -o evergreen main.o -L/usr/lib -lboost_python-py27 -lpython2.7 -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions
	mv evergreen ..
main.o : main.cpp
	g++  -ftemplate-depth-128 -O0 -fno-inline -Wall -I/usr/include -I/usr/include/python2.7 -c -o main.o main.cpp
