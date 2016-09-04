
CFLAGS = -std=c++11 -lstdc++ -Wall -I./sql-parser-1.4/src/ -L./sql-parser-1.4/

all:
	$(CXX) $(CFLAGS) main.cpp -o sql -lsqlparser

