# high performance

## Table of contents
- [Abstract](#abstract)
- [Experiment content](#experiment-content)
- [Analysis](#analysis)
- [Implementation](#implementation)
- [Table and flow charts](#table-and-flow-charts)

### Abstract

This project mainly describes the use of python language to simulate parallel and distributed computing. Divide a large computing task into several small tasks, and then send these different small computing tasks to other computing nodes through a management node. Each computing node obtains the calculation results, and sends each calculation result to one of them. Computing nodes, summarized by the computing node, and finally send the result back to the control node

### Experiment content

**Content**: Given a natural number range 2-n, calculate how many prime numbers there are in the range and the time consumed by the entire calculation process


**Input**: need to calculate the maximum number of prime numbers n


**Output**: the total number of prime numbers in the range s and the total consumption time t

### Analysis

+ After the management node sends the computing code to each computing node, the computing code is the same for each computing node, so how does each computing node know its own computing task

+ After each computing node completes the computing task, how to send the partial result of the calculation to the designated computing node

+  How the specified computing node collects the results sent by other computing nodes

+ How the designated computing node sends the final summary result to the management node

### Implementation

This experiment is mainly implemented by Python language, which uses socket module, multithreading and message queue in Python language to simulate management node and calculation node. The management node is the client, and the calculation node is the server. There are 4 files in this experiment, respectively.

1.File 20185227018Control.py as the management node
2.File 20185227018Node.py file for the compute node
3.The code file 20185227018.py that needs to be executed has two parameters, which are calculating the node number and the total number of nodes respectively
4.Hosts.txt file that holds the IP addresses of all compute nodes

### Table and flow charts

