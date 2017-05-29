# GProg
## How to run

First, make sure Python is installed.
```
  > sudo apt-get install python2.7
```
Then, install PLY:
```	
  > sudo apt-get install python-ply
```
Next, compile the virtual machine
```
> g++ -std=c++11 Source.cpp -o virtualMachine.out
```
Next compile the GProg code:
```
> python parser.py filename.gp
```
Finally, run the virtual machine
```
> ./virtualMachine.out
```
