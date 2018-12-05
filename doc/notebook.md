# Diary Timothy Bergström Course BB2490


2018-11-27
----
### 18:00

First entry and creation of project diary. My idea is to have it in github,
since it will be easy to follow any commits and timeline of project.



2018-11-29
----
### 13:30

First meeting, and we created the project plan. Our plan is to first familiarize ourselfs with the programs, then try to recreate two plots with the data from the paper.



2018-12-01
----
### 16:00

I got a license for MaxQuant and installed it on my computer and installed it.
I'm about to install quandenser, and my idea is to make an ssh server which the other in my group can log into.

### 16:30

I've been struggling with installing Quandenser. The command "git clone --recursive https://github.com/statisticalbiotechnology/quandenser.git" seems to breaks when try it.
Sometimes it says "Public key" is denied and other times that "Connection error". I tested on multiple networks, so I cant be that.

### 16:45

It seems to be something strange when cloning the other modules. No matter, I manually cloned each one with "git clone <LINK_TO_REPO>".
It seems to install now, but it crashes when fixing boost.



2018-12-02
----
### 13:00

I cant make it install. It seems to not be able to find the library files. I tried to include "-BOOST\_LIBRARY\_DIR=$build_dir/tools/lib" in "admin/builders/ubuntu64\_build.sh" but it does not work.
I'll send an email to Lukas tomorrow if I can't get it to work.

### 13:40

I went into "ubuntu64_build.sh" and enabled "-DBoost_DEBUG=1" in the cmake line. The output seems to crash when trying to import the "boost.atomic" library file.
I'm currently downloading "boost" independently with the command "sudo apt-get install libboost-all-dev". 

### 13:50

I deleted the "build" folder which is installed when running ./quickbuild.sh and am currently rerunning the script.
This might take some time before I see the results, hopefully it works now.


### 14:10

Well, the error with the boost is gone, but now theres something else crashing...
The error was "Cannot create module Dinosaur, mvn execution failed"

### 14:30

Percolator and maracluster compiles fine
Something is crashing on this line in CMakeLists:

>"execute_process(COMMAND mvn package -Pconf -DskipTests -Ddir=${CMAKE_CURRENT_BINARY_DIR}/dinosaur WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/ext/dinosaur RESULT_VARIABLE MVN_RESULT)"

The "mvn" is a java tool. I thought I already installed java with "apt-get install default-jdk" with version openjdk 10.0.2, but Ill reinstall it and see what happens.

### 14:50

Reinstalling java did not work, but installing maven with *sudo apt install maven* made it run. However it crashed once again...

>Failed to execute goal org.scala-tools:maven-scala-plugin:2.15.2:compile (default) on project Dinosaur: wrap: org.apache.commons.exec.ExecuteException: Process exited with an error: 1(Exit value: 1) -> [Help 1]"

using mvn -X to get full debug, it seems that some dependencies are missing.

### 15:00

Okay, default-jdk is "openjdk" which is not the same as oracles own like I thought it was. Installing oracles java after purging openjdk makes dinosaur compile. However, there is another error, once again...

>maracluster/CMakeFiles/maracluster.dir/build.make:113: recipe for target 'maracluster/maracluster' failed

>[ 29%] Linking CXX executable maracluster crashes here

Apperently maracluster fails due to "unreferenced" dependencies in some compiled functions. Perhaps the other boost libraries are making the crashes?

### 20:40

I just can't get it to work. I've tried a lot of stuff, purging the old boost files and trying to make FindBoost find the static libraries, but to no avail.



2018-12-03
----
### 14:20

I got it to work with the help of Lukas Käll and Patrick Truong. Instead of compiling everything from scratch, I forgot to look at the "releases" folder where the .deb files are stored. My fault.

I also found what the problem was with both the compilation and the --recursive issues.
The problem was intranet-issues + antivirus. I tried to install on both my laptop and my desktop on 2 networks, my home router and using my phone as a hotspot by sharing the 4g connection.
I had added a ssh-key to my account beforehand for both laptop and desktop, so it was not that problem.

The AV blocked some packages from downloading (for some reason) making the dependencies fail. I deactivated my AV beforehand to test whether that was the problem after a fresh Ubuntu installation and the packages installed correctly.
The intranet blocked incoming traffic from port 22 for some reason, even though I had the port-forwarded to my computer. I tried to force the ssh to use port 443 instead in the /etc/ssh/ssh_config, but with the same issues.
The phone did it as well, but later found out that [using ssh from a hotspot does not work](https://android.stackexchange.com/questions/120819/ssh-tunnel-through-android-device)

So this means that neither networks worked.

However, I went to school and tested it on the network there. Now, downloading the repos recursively works fine (since there is no block when using the intranet in school). The AV does not block any packages, since it is deactivated.
However, the problem with Boost libraries persist. It still says:


	CMake Error at /usr/share/cmake-3.10/Modules/FindBoost.cmake:1947 (message):
	  Unable to find the requested Boost libraries.

	  Boost version: 1.56.0

	  Boost include path:
	  /mnt/c/Users/timot/Downloads/BB2490/build/ubuntu64/tools/include

	  Could not find the following static Boost libraries:

			boost_filesystem
			boost_iostreams
			boost_regex
			boost_thread
			boost_serialization
			boost_system
			boost_chrono

	  Some (but not all) of the required Boost libraries were found.  You may
	  need to install these additional Boost libraries.  Alternatively, set
	  BOOST_LIBRARYDIR to the directory containing Boost libraries or BOOST_ROOT
	  to the location of Boost.
	Call Stack (most recent call first):
	  ext/maracluster/src/CMakeLists.txt:22 (find_package)

  
However, the .deb file works, so it doesn't matter at the moment.

### 15:10

I really wanted to see what the problem was with the libraries, so I continued to debug it.
I found why the boost libraries does not compile. It was pretty simple:
I had gcc installed from before (I have a course in C programming) and I tested on a non-fresh install of ubuntu, 
so FindBoost detects that I have gcc7 installed, thus it looks for files named:

*libboost_filesystem-gcc7-mt-s.a*

while the lib files are called 

*libboost_filesystem-gcc-mt-s.a*

The output of the terminal when gcc have not been renamed has been added to *terminal_output* folder with the name *gcc_problem.txt*

Adding "7" to all filenames with gcc in them made it work. I successfully compiled the .deb file (which was already found in the release folder in github)
Maybe I'll test it on a fresh install of ubuntu to see if the problem persist, maybe it was just a collision between already installed gcc.

### 17:20

Yes, a fresh install of ubuntu gave the same output. Maybe some change in a dependency made FindBoost look for gcc7 files instead, or proteowizard 

### 18:00

There's a total of 147,3 GB of files in mzML format in PRIDE, but there are about three times more data in RAW format (quandenser uses mzML files).
Instead of downloading every RAW file by itself and converting it to mzML, I created a simple python script that downloaded the files one after the other.
The script can be find in /bin. I also created a simple .sh script that outputs a batch.txt with full path to the mzML files, which quandenser uses.
Downloading all the data will take about 24 hours.


2018-12-04
----
### 14:00

I ran quandenser with the test data over night and it took about 2 hours to complete.

>Output: Running Quandenser took: 7411.55 cpu seconds or 7369 seconds wall time

The ouput of the terminal has been added to results/example with the .tsv files which tiqluer outputs.

The test data sets were about 4.02 Gb in size. If the run time is linear, this means computing 147 Gb worth of MS data would take about 74 hours (in best case).
I'll discuss in the meeting if we could divide the data files so each group member can take a part of the set and do the calculation to speed it up.

I also discovered that quandenser can take batch.txt in the format <PATH\_TO\_mzML> <A/B> where A or B seems to correspond to sample (ex. cell colony in environment)
so the .sh file might not work. I need to investigate further if I have understood it correctly.

### 17:00

Our group had a meeting where we discussed the project. We sent a mail to Michael Jahn about some questions about the data file naming and our project plan.
My group members will also try to calculate the example set, to see if they get the same output.
We also talked briefly about dividing the data sets to minimize computational time. 

### 21:50

I will try and record the CPU and RAM usage of quandenser, and maybe dial down the RAM allocated to Dinosaur. Perhaps I could run two parallel processes at once, each process
calculating a couple of mzML files (such as light/co2).

PS: If we use Crux, we could use *Synechocystis_PCC6803.fasta* as the fasta database


2018-12-05
----
### 9:30

I ran quandenser on "20170419\_GM\_Cyano\_1000\_R1\_BC1\_01\_2485.mzML". It crashed after 6 hours. I added the crash log to results/testrun
Looking at quandensers defaults, it uses 24GB by default, while my computer only has 16GB. Ill try to run it again

### 10:30

No matter what I do seems to make it work. When I try to run it on the file, it returns this

>java.lang.OutOfMemoryError: GC overhead limit exceeded[INFO] [12/05/2018 08:40:36.719] [actor-system-scheduler-1] [ActorSystem(actor-system)] starting new LARS thread

And that was when I set it to 16Gb of memory (using command "--dinosaur-memory 16G")


### 11:00

The files used in the example is 0.5 Gb while the one I tried was 2.6 Gb. When I try to run just the 0.5 Gb file, it works fine. Perhaps I could split the mzML file into
many smaller parts and run them in a batch, annotating that they are all from the same sample (adding A to the end in the batch file). First, I need to research if it even is possible
to split mzML without losing data. If it is possible, I could try to make a XML parser that divides sections into files, if I can learn more about the structure and what to include in each file
mzML files.

### 17:00

My group members have the same problem as me with the ram issue. I still haven't found a way to split the files.

Also, I found a way to fix the gcc issue when compiling, by adding this line after line 78 in admin/builders/ubuntu64\_build

	find ../lib -name '*gcc*' -exec bash -c ' gcc\_name="gcc$(gcc -dumpversion)"; mv $0 ${0/gcc/$gcc\_name}' {} \;

I tried it on a toy example, and it should work when compiling.

