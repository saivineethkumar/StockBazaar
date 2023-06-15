[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=10125712&assignment_repo_type=AssignmentRepo)
Compsci 677: Distributed and Operating Systems

Spring 2023

# Lab 1: Asterix and the Stock Bazaar

## Goals and Learning Outcomes

This lab has the following learning outcomes with regard to concepts covered in class.

1) Learn to design distributed client-server applications
2) Learn to design a concurrent networked server application
3) Learn to design your own thread pool for servers and use thread pool abstractions provided by
   major languages
4) Learn to design distributed applications using a low-level abstraction of socket communication as
   well as high-level abstraction of remote procedure calls.

The lab also has the following learning outcomes with regards to practice and modern technologies

5) Learn to use gRPC, a modern RPC framework
6) Learn to measure the performance of a distributed application
7) Learn to use version control and build tools

## Instructions

1) You may work in groups of two for this lab. If you decide to work in groups, you should briefly
   describe how the work is divided between the two team members in your README file.
2) You can use either Python or Java for this assignment. You may optionally use C++, but TA support
   for C++ issues will be limited.
3) Do's and don'ts:
   - discuss lab with other students: allowed
   - use of AI tools: allowed with attribution (be sure to read policy in course syllabus)
   - use code from others/Internet/friends/coders for hire: disallowed
   - ask TAs for clarifications/help: always allowed

## Lab Description

The year is 50 B.C.  The Gauls, led by Asterix, have been in confined to their homes to limit their exposure to a pandemic caused by a mysterious germ spread by rotting fish sold by Unhygienix the fish-monger. To pass time in their homes, Gauls have taken up trading meme stocks in their local stock bazaar. Obelix (a sculptor by profession) has tasked by the village chief  to run the stock trading server. Every Gaul now has a stone tablet that allows them look up to latest stock prices of their favorite meme stock. Each smart-stone (not to be confused with a smart-phone, which are yet to be invented) also allows  stock purchases from Obelix's stock trading server.  Cacofonix, the village bard, is responsible for providing Obelix's server with live updates of stock prices, which he does by singing the prices from the stock bazaar and thereby sending updated prices to the server.


This lab has three parts (two programming parts and one performance measurement/evaluation part). In
the first part, you will design your own thread pool and use it to write a simple client-server
application for the above problem that uses network sockets. This part will give you an appreciation of how thread pools
work internally. In the second part, you will use gRPC and built-in thread pool mechanisms to write
the client-server application. This part will give you an appreciation of using modern frameworks to
write distributed applications, since most programmers simply use higher-level abstractions such as
built-in thread pools and RPCs rather than implementing their own thread pool or using lower-level
abstractions such as sockets.

## Part 1: Implementation with Socket Connection and Handwritten Thread Pool

In this part, you need to implement online stock trading  as a socket-based client-server application.

The server component should implement a single method Lookup, which takes a single string argument
that specifies the name of the stock company. The Lookup query returns the price of the meme stock (as a floating-point value, such as 15.99). It returns -1 if the company name is not found and returns 0 if the name is found, but trading is suspended due to excessive meme stock trading by the Gauls.  Since part 1 only
involves lookups and no trading, the return value of 0 (i.e., suspension of trading) is only relevant for part 2.

The client component should connect to the server using a socket connection. It should construct a
message in the form of a buffer specifying the method name (e.g., string "Lookup") and arguments
("stockName"). The message is sent to the server over the socket connection. The return value is
another buffer containing the price of the stock or an error code such as -1 and 0, as noted above.

The server hosts the world's smallest stock market that traders only two meme stocks: (i) GameStart and (ii) FishCo,
both popular local businesses. It maintains a catalog that includes these
stock names, the current price of each stock, and the trading volume (number of stocks traded so far that day) in an in-memory data structure
(this part does not require a database backend for your  application's stock catalog).

The server should listen on a network port of your choice (e.g., a high port number such as 8888),
accept incoming client requests over sockets, and assign this request to an idle thread in the
thread pool. The main part of the assignment is to implement your own ThreadPool (**you are not
allowed to use a ThreadPool framework that is available by the language/libraries**). The thread
pool should create a static number of threads that is configurable at start time, and these threads
wait for requests. The main server thread should accept requests over a socket and insert them into
a request queue and notify the thread pool, which causes one of the idle threads to be assigned this
request for processing. Your design should include the request queue, threading code for the thread
pool, and any synchronization needed to insert or remove requests from the queue and notify threads.

The client should be a for-loop that sequentially issues query requests to the server. You design
should be able to have multiple client processes making concurrent requests to the server, thereby
exercising the thread pool.

Note: You are allowed to look at sample implementations of thread pools that are available on the
Internet, but in the end, your code should be your own work and should not include snippets of code
written by others. We have a comprehensive list of sample implementations that can be found on the
Internet and will be strictly checking for violations of this policy. If you read some docs or
looked at code found on the Internet, please credit all such sources by listing them in a Reference
section.

## Part 2: Implementation with gRPC and Built in Thread Pool

In this part, you need to implement our online stock trading server using gRPC and built-in thread
pool support.

The server component should implement three gRPC calls:
   1. `Lookup(stockName)`, which takes the string stockName and returns the price of the stock and
   the trading volume so far. The method returns -1 as the price if an invalid stock name is specified.
   2. `Trade(stockName, N, type)`, which buys or sells N items of the stock and increments the trading volume of
   that item by N. The type parameter should indicate buy or sell. The method returns 1 if the call succeeds, 0 if stock trading is suspended, and -1 if an invalid stock name is specified. The maximum allowed trading volume should be a configurable parameter per stockName specified at program startup time.
   3. `Update(stockName, price)`, which updates the stock price every so often. The method returns 1 if the update is successful, -1 if an invalid stock name is specified, and -2 if an invalid price (e.g, negative value) is specified. 

You should use protobuf to create appropriate message structures for arguments and return values of
both calls, and design rpc methods as noted above. The stock catalog should be expanded to four
stocks. In addition to GameStart and FishCo, the catalog should also include BoarCo (for Boar
lovers) and MenhirCo (for Menhir fans).

Implement your gRPC server using a built-in thread pool. You do not need to write your own thread
pool and should instead use the built-in dynamic thread pool support. Since the thread pool is
dynamic, set an appropriate max limit on the maximum number of concurrent RPCs when you start your
server. Use appropriate synchronization methods on the stock catalog since querying and buying will
read from and write to the catalog, which make it a shared data structure. The stock catalog can be
maintained in memory and no database backend is needed for this lab. Implement appropriate
error/exception handling as needed for your design (for example, a stock may be actively traded when
queried but occasionally trading may be suspended on a subsequent trade request if excessive trading
volume is observed).

The client component should use gRPC to make lookup and trade calls to the server. The client can be
a for loop that sequentially issues either lookup or trade request. You design should be able to
have multiple client processes making concurrent requests to the server, thereby exercising the
thread pool. Separately, implement a special client makes periodic updates to stock prices at random
times. This client only makes updates to prices and does not make any trades.

## Part 3: Evaluation and Performance Measurement

For each part, perform a simple load test and performance measurements. The goal here is understand
how to perform load tests on distributed applications and understand performance. Deploy multiple
client processes and have each one make concurrent requests to the server. The clients should be
running on a different machine than the server (use the EdLab, if needed). Measure the latency seen
by the client for different types of requests, such as lookup and trade.

Vary the number of clients from 1 to 5 and measure the latency as the load goes up. Make simple
plots showing number of clients on the X-axis and response time/latency on the Y-axis. Be sure to
show the response times of lookup and trade requests separately for part 2.

Using these measurements, answer the following questions:

1) How does the latency of Lookup compare across part 1 and part 2? Is one more efficient than the
   other?
2) How does the latency change as the number of clients (load) is varied? Does a load increase
   impact response time?
3) How does the latency of lookup compare to trade? You can measure latency of each by having
   clients only issue lookup requests and only issue trade requests and measure the latency of each
   separately. Does synchronization pay a role in your design and impact performance of each? While
   you are not expected to do so, use of read-write locks should ideally cause lookup requests (with
   read locks) to be be faster than trade requests (which need write locks). Your design may differ,
   and you should observe if your measurements show any differences for lookup and trade based on
   your design.
4) In part 1, what happens when the number of clients is larger the size of the static thread pool?
   Does the response time increase due to request waiting?

## What to submit.

1) Your solution should contain source code for both parts separately. Inside the `src` directory,
   you should have two folders named "part1" and "part2" for the two parts. Submit your code with
   good inline comments.

2) Submit the following additional documents inside the `docs` directory. 1) A Brief design document
   (1 to 2 pages) that explains your design choices (include citations, if you used referred to
   Internet sources), 2) An Output file (1 to 2 pages), showing sample output or screenshots to
   indicate your program works, and 3) An Evaluation doc (2 to 3 pages), for part 3 showing plots
   and making observations.

3) Submit all of the above via GitHub classroom. Include a README at the top level explaining how to
   build and run your code on Edlab (if we can not run it, we can not grade it). It's recommended to
   use a build tool and include your build file in the repo if you are using java (e.g., gradle or
   maven) or C++ (e.g., make or cmake). For Python, it's optional to use a build tool, but
   `requirements.txt` should be included if your code has external dependencies.

4) Your GitHub repo is expected to contain many commits with proper commit messages (which is good
   programming practice). Use GitHub to develop your lab and not just to submit the final version.
   We expect a reasonable number of commits and meaningful commit messages from both members of the
   group (there is no "target" number of commits that is expected, just enough to show you are using
   GitHub as one should).

## Grading Rubric

1) Part 1 and Part 2 are each 42.5% of the lab grade.

   For full credit:

   * Source code should build and work correctly (20%),
   * Code should have in-line comments (5%),
   * A design doc should be submitted (7.5%),
   * An output file should be included (5%)
   * GitHub repo should have adequate commits and meaningful commit messages (5%).

2) Part 3 is 15% of the grade.

   For full credit:

   * Eval document should be turned in with measurements for Part 1 and 2 (shown as plots where
     possible and tables otherwise) (7.5%)
   * Explaining the plots by addressing answers to the 4 questions listed in Part 3 (7.5%).

Late policy will include 10% of points per day. Medical or covid exceptions require advance notice,
and should be submitted through pizza (use exceptionRequests folder in pizza). Three free late days
per group are available for the entire semester - use them wisely, and do not use them up for one lab
by managing your time well.

## References

- Who are the Gauls? https://en.wikipedia.org/wiki/Asterix
- What are meme stocks? https://en.wikipedia.org/wiki/Meme_stock
- Tutorial to gRPC in Python https://grpc.io/docs/languages/python/basics/
- Tutorial to gRPC in Java https://grpc.io/docs/languages/java/basics/
- Tutorial to gRPC in C++ https://grpc.io/docs/languages/cpp/basics/
- Learn about Git and GitHub https://docs.github.com/en/get-started/using-git/about-git
- Learn about python's built in threadpool https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor
- Learn about java's built in threadpool https://docs.oracle.com/javase/tutorial/essential/concurrency/pools.html
