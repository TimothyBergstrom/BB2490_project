# Diary Timothy Bergström Course BB2490

### 2018-11-27, 18:00

First entry and creation of project diary. My idea is to have it in github,
since it will be easy to follow any commits and timeline of project.

### 2018-11-29, 13:30

First meeting, and we created the project plan. Our plan is to first familiarize ourselfs with the programs, then try to recreate two plots with the data from the paper.


### 2018-12-01, 16:00

I got a license for MaxQuant and installed it on my computer and installed it.
I'm about to install quandenser, and my idea is to make an ssh server which the other in my group can log into.


### 2018-12-01,16:30

I've been struggling with installing Quandenser. The command "git clone --recursive https://github.com/statisticalbiotechnology/quandenser.git" seems to breaks when try it.
Sometimes it says "Public key" is denied and other times that "Connection error". I tested on multiple networks, so I cant be that.


### 2018-12-01, 16:45

It seems to be something strange when cloning the other modules. No matter, I manually cloned each one with "git clone <LINK_TO_REPO>".
It seems to install now, but it crashes when fixing boost.


### 2018-12-02, 13:00

I cant make it install. It seems to not be able to find the library files. I tried to include "-BOOST_LIBRARY_DIR=$build_dir/tools/lib" in "admin/builders/ubuntu64_build.sh" but it does not work.
I'll send an email to Lukas tomorrow if I can't get it to work.


### 2018-12-02, 13:40

I went into "ubuntu64_build.sh" and enabled "-DBoost_DEBUG=1" in the cmake line. The output seems to crash when trying to import the "boost.atomic" library file.
I'm currently downloading "boost" independently with the command "sudo apt-get install libboost-all-dev". 


### 2018-12-02, 13:50

I deleted the "build" folder which is installed when running ./quickbuild.sh and am currently rerunning the script.
This might take some time before I see the results, hopefully it works now.


### 2018-12-02, 14:10

Well, the error with the boost is gone, but now theres something else crashing...
The error was "Cannot create module Dinosaur, mvn execution failed"


### 2018-12-02, 14:30

Percolator and maracluster compiles fine
Something is crashing on this line in CMakeLists:

"execute_process(COMMAND mvn package -Pconf -DskipTests -Ddir=${CMAKE_CURRENT_BINARY_DIR}/dinosaur WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/ext/dinosaur RESULT_VARIABLE MVN_RESULT)"

The "mvn" is a java tool. I thought I already installed java with "apt-get install default-jdk" with version openjdk 10.0.2, but Ill reinstall it and see what happens.


### 2018-12-02, 14:50

Reinstalling java did not work, but installing maven with "sudo apt install maven" made it run. However it crashed once again...

"Failed to execute goal org.scala-tools:maven-scala-plugin:2.15.2:compile (default) on project Dinosaur: wrap: org.apache.commons.exec.ExecuteException: Process exited with an error: 1(Exit value: 1) -> [Help 1]"

using mvn -X to get full debug, it seems that some dependencies are missing.


### 2018-12-02, 15:00

Okay, default-jdk is "openjdk" which is not the same as oracles own like I thought it was. Installing oracles java after purging openjdk makes dinosaur compile. However, there is another error, once again...

maracluster/CMakeFiles/maracluster.dir/build.make:113: recipe for target 'maracluster/maracluster' failed

[ 29%] Linking CXX executable maracluster crashes here

Apperently maracluster fails due to "unreferenced" dependencies in some compiled functions. Perhaps the other boost libraries are making the crashes?


### 2018-12-02, 20:40

I just can't get it to work. I've tried a lot of stuff, purging the old boost files and trying to make FindBoost find the static libraries, but to no avail.

