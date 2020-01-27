# Compiler
Project for a course titled 'Formal Languages And Translation Techniques'
(Języki Formalne i Techniki Translacji) at the Faculty of Fundamental Problems of Technology (WPPT), 
Wrocław University of Science and Technology (PWr). This course is for 5th semester of computer science
studies.

### Repository content
The _src_ folder contains source code for the project, tests. _Examples_ folder 
contains example programs which are written in imperative language which can
be compiled with this compiler and then executed on virtual machine.
_Maszyna_wirtualna_ is the folder containing virtual machine.
The source code of virtual machine was written by the course lecturer - Maciej
Gębala. All the content in the folder _maszyna_wirtualna_ belongs to him.
Virtual machine has two versions: classic and dedicated to big numbers (running
it requires installation of additional package). More info about
requirements and task specification in _labor4.pdf_ file.  
 
Some tests in _srs/utils_test_ folder are neither refactored nor working yet. There is a plan 
to make them work in the future and adjust them to the newest version of the
compiler.


### Used tools and libraries
Python 3.7 and SLY library are required to run the compiler.
SLY (Sly Lex Yacc) is the library for writing parsers and compilers.
CLN (Class Library for Numbers) is required to build virtual machine dedicated for big numbers.

### Packages installation
Example installation of the packages on Ubuntu.  
Update apt-get and then install python 3.7:
```
$ sudo apt-get update
$ sudo apt install python3.7
```
Install pip (standard package manager for Python packages) and then install SLY using pip for Python 3.7:
```
$ sudo apt-get install python3-pip
$ pip3 install sly
```
If you want to use virtual machine working on big numbers, you need to install cln library:
```
$ sudo apt-get install libcln-dev
```  


### Launching the compiler
Go to root folder (repository folder).  
Build virtual machine (1) or virtual machine for big numbers (2):
```
(1) $ make maszyna_wirtualna/maszyna-wirtualna
(2) $ make maszyna_wirtualna/maszyna-wirtualna-cln
```
Run compiler:
```
$ python3.7 src/parser.py source_filename output_filename
```
Use virtual machine (classic or big numbers) to run the generated code:
```
$ ./maszyna_wirtualna/maszyna-wirtualna output_filename
$ ./maszyna_wirtualna/maszyna-wirtualna-cln output_filename
```
