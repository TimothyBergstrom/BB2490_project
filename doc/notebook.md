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

Also, I found a way to fix the gcc issue when compiling, by adding this line after line 78 in admin/builders/ubuntu64\_build.sh

	find ../lib -name '*gcc*' -exec bash -c ' gcc_name="gcc$(gcc -dumpversion)"; mv $0 ${0/gcc/$gcc_name}' {} \;

I tried it on a toy example, and it should work when compiling.

### 18:00

I found something called "OpenMS" which can split and handle mzML. I also found that it has Perculator included, which I thought was pretty neat. I'm installing it now.

Running quandenser with dinosaur using 15Gb seems to work, it has calculated for about one hour without a crash, but is still on the first step.



2018-12-06
----
### 17:00

We had a meeting in the group and discussed the how we should proceed with the project. We concluded that calculating everything from scratch is not reasonable at this rate and 
that we'll look into MaxQuant while we look for solutions to the problems with Quandenser. We also finished the presentation for tomorrow.

The OpenMS MzMLSplitter does not work with quandenser. The first problem is that a file of 2.6 Gb is split into many files with a total of about 4.5 Gb. The second problem is that 
this solves the RAM issue with dinosaur, but it instead crashes on maracluster. Also, the dinosaur calculations with the splitted files are very slow.

I'm making a simple script that splits mzML files, by using an example mzML file provided by PRIDE (the mzML example is in the data folder and the script in the bin folder)

### 20:45

I finshed the mzML splitter, it is spaghetticode in galore and really badly written, but it works. About 4 times slower than mzMLSplitter from OpenMS, but its a start. I tried to speed it up with C code in some parts,
but the performance increase was negligible. Running the splitted files through quandenser seems to work with dinosaur at least, but it is extremely slow. Hopefully, it will get through maracluster as well.

Perhaps I will split the example mzML files and compare the outputs to find any errors the split might have on the code (if the splitted files will go through quandenser)

### 21:30

The mzML splitter worked for dinosaur, which completed sucessfully. However, maracluster still crashes with output:

maracluster batch --splitMassChargeStates --batch batch_list.txt --clusterThresholds -10.0 --pvalThreshold -10.0 --output-folder Quandenser_output/maracluster
Started Thu Dec  6 21:33:45 2018

	Splitting spectra by precursor Mz
	Accumulating peak counts and precursor Mzs
	  Processing   Processing split3_20170419_GM_Cyano_60_R2_BA2_01_2466.mzML (40%).
	  Processing split6_20170419_GM_Cyano_60_R2_BA2_01_2466.mzML (70%).
	  Processing split7_20170419_GM_Cyano_60_R2_BA2_01_2466.mzML (80%).
	  Processing split2_20170419_GM_Cyano_60_R2_BA2_01_2466.mzML (30%).
	split1_20170419_GM_Cyano_60_R2_BA2_01_2466.mzML (20%).
	  Processing split4_20170419_GM_Cyano_60_R2_BA2_01_2466.mzML (50%).
	  Processing split5_20170419_GM_Cyano_60_R2_BA2_01_2466.mzML (60%).
	  Processing split0_20170419_GM_Cyano_60_R2_BA2_01_2466.mzML (10%).
	terminate called recursively
	terminate called recursively
	Aborted (core dumped)
	
However, I noticed that the example mzML files all have one chromatogram, while the mzML from PRIDE does not. Is this the problem which causes the crashes in maracluster?

### 22:00

I tried MaxQuant and can't get it to work either... I follow the instructions how to run it, but it crashes unexpectedly all the time. I tested on example mzML sets, it crashes. I try to open visualisation of data,
it crashes. I tested on the tiny mzML test file from PRIDE, but that crashes it as well. I can't find any crash logs or anything like that which specifies why it crashes...


2018-12-10
----
### 22:40

We have booked a meeting with Michael Jahn tomorrow at 15:00. We will speak to him about the RAM problem. I have also tried to convert .baf to .mzML, but proteowizard and OpenMS doesn't have that capabilities.
I tried to register an account on Bruker.com (aka the company that makes the ToF-MS used to generate the experiments) to download compassXport, but I have not received a confirmation mail yet.


2018-12-11
----
### 21:40

We had our meeting with Michael Jahn today and had a tour in the lab. He also gave us a reduced mzML data set, which seems to not be compatible with quandenser (it crashed on maracluster, like the last time, the output is added to the results/reduced folder).
We don't know which problem causes it, but it seems that using Comet to analyse the mzML files agaisnt the database, it returns nothing (aka no matches), which might be the problem.
Michael he showed us some tools we could use to create a pipeline for analysing the data using KNIME and OpenMS. Hopefully, we can get some of it working this week or during the winter break.

### 22:40

Using a retention window of the mzML files from 3600 seconds to 4800 seconds (aka start 1 hour into the MS and 20 minutes forwards) crashed on maracluster, as before. Using Cruxadapter and MSGFPlusAdapter didn't work. Perhaps I set them up wrong in KNIME.


2018-12-12
----
### 12:00

I found something that might create the problem. Using the mzML files (full retention time) through MSFGPlusAdapter works fine and I get an output.
However, when I set the retention time to from start to max retention time of the mzML file using "FileFilter" in OpenMS, I get some strange results.

Firstly, the file size doubles (from 2.6 Gb to 5.2 Gb). Using the mzML analyser script that I created, I get these outputs:

	NON-FILTERED mzML 2.6 Gb (the files from PRIDE)
	Counted 8463051 lines
	168298 spectrums and 0 chromatograms
	168298 indices for spectrum
	0 indices for chromatogram
	it took 31.99 seconds with Python

	FILTERED mzML 5.2 Gb (retention time 1 second to max retention time)
	Counted 7661733 lines
	168298 spectrums and 0 chromatograms
	168298 indices for spectrum
	0 indices for chromatogram
	it took 40.22 seconds with Python

The filtered has a larger file size, even though the amount of lines in the file is less than the other. Perhaps something is wrong with my script, but counting lines in files should always be the same, so maybe each line is larger.
A made a quick script to get average line lengths, and that seems to be the case.

	NON-FILTERED
	311.901 is the average line length

	FILTERED
	681.027 is the average line length

Secondly, running the Filtered mzML files through MSFGPlusAdapter doesn't work, even if I set the retention time to the same window as the source. This means that the root to our problems seems to lie when we are trying to reduce the mzML files.
Perhaps there is a setting in the FileFilter which I missed. I will check on it.

http://ftp.mi.fu-berlin.de/pub/OpenMS/release1.9-documentation/html/TOPP_FileFilter.html 


### 18:00

I used the XMLValidator tool from OpenMS and tested on the mzML files from PRIDE and the files which had gone through the FileFilter.

FROM PRIDE

	Validating mzML file against schema version 1.1.0
	Validation error in file '20170419_GM_Cyano_60_R2_BA2_01_2466.mzML' line 50 column 25: missing elements in content model '(source+,analyzer+,detector+)'
	Validation error in file '20170419_GM_Cyano_60_R2_BA2_01_2466.mzML' line 8463047 column 13: empty content is not valid for content model '(offset+)'
	Failed: errors are listed above!
	XMLValidator took 01:06 m (wall), 01:06 m (CPU), 1.00 s (system), 01:05 m (user).
	
	
GONE THROUGH FILEFILTER

	Validating mzML file against schema version 1.1.0
	Success: the file is valid!
	XMLValidator took 01:02 m (wall), 01:02 m (CPU), 0.94 s (system), 01:01 m (user).
	
I also parsed through the files quickly and compared them. It seems that the FileFilter changes the files slightly, but I cannot spot what the change is that makes MSFGPlusAdapter crash.

### 18:30

If I enabled "zlib compression" in the FileFilter, the file sizes become comparable to the source files.
I also compared the files with FileInfo (a module in OpenMS) and the one results are exactly the same for the source files and the files which had gone through FileFilter (added to results/2018-12-12_FileInfo_comparsion)


2018-12-28
----
### 13:30

Got back from the winter break and can now work on the project


2018-12-30
----
### 20:00
I uploaded a new KNIME workflow in the bin/KNIME folder, which considers only matches with FDR < 0.01, which uses a generated DecoyDatabase.
It seems to work fine. I get less matches with FDR, but that is expected. I will try to run it on all the samples (I took scan time 3000 - 4800 on every replicate1 for all points)


2018-12-31
----
### 18:00
I finished the calculations of KNIME with MSGFPlusAdapter, CometAdapter and CruxAdapter with FDR < 0.01. I am now doing the calculations on quandenser, but I was met by a strange crash.
Calculations were made in 6 files in dinosaur (when "hill reports" are being written), but I got this error message:

	 A fatal error has been detected by the Java Runtime Environment:
	
	  SIGSEGV (0xb) at pc=0x00007f6d61026313, pid=226, tid=0x00007f6d4fbd0700
	
	 JRE version: Java(TM) SE Runtime Environment (8.0_191-b12) (build 1.8.0_191-b12)
	 Java VM: Java HotSpot(TM) 64-Bit Server VM (25.191-b12 mixed mode linux-amd64 compressed oops)
	 Problematic frame:
	 j  scala.runtime.BoxesRunTime.unboxToDouble(Ljava/lang/Object;)D+9
	
	 Failed to write core dump. Core dumps have been disabled. To enable core dumping, try "ulimit -c unlimited" before starting Java again
	
	 An error report file with more information is saved as:
	 /mnt/d/Downloads/BB2490/data/mzML_reduced_own/Quandenser/hs_err_pid226.log
	
	 If you would like to submit a bug report, please visit:
	   http://bugreport.java.com/bugreport/crash.jsp
	   
I put the whole error message in results/2018-12-31_dinosaur_weird_crash. Perhaps something went wrong with the file.
The file I used was "20180112_60_ja8_r1_GE2_01_5509.mzML"

### 18:50
I reran the program and it got through the failed file, but now it crashed on 4 after that file, but the crash code was different. What might be the problem?
I have uploaded both crash files and also the batch file.


2019-01-02
----
### 18:00
2 crashes found in triqler.
First crash: batch_list.txt need a group name and also cannot end with an empty line (crashes the parser in triqler, after some debugging)
Second crash: Groupnames are entered correctly, no empty lines and everything went through quandenser and crux correctly. Gives this:

	Traceback (most recent call last):
	  File "/usr/lib/python2.7/runpy.py", line 174, in _run_module_as_main
		"__main__", fname, loader, pkg_name)
	  File "/usr/lib/python2.7/runpy.py", line 72, in _run_code
		exec code in run_globals
	  File "/usr/local/lib/python2.7/dist-packages/triqler/__main__.py", line 8, in <module>
		main()
	  File "/usr/local/lib/python2.7/dist-packages/triqler/triqler.py", line 36, in main
		runTriqler(params, args.in_file, args.out_file)
	  File "/usr/local/lib/python2.7/dist-packages/triqler/triqler.py", line 104, in runTriqler
		diff_exp.doDiffExp(params, peptQuantRows, triqlerOutputFile, getPickedProteinCalibration, selectComparisonBayesTmp, qvalMethod = qvalMethod)
	  File "/usr/local/lib/python2.7/dist-packages/triqler/diff_exp.py", line 17, in doDiffExp
		proteinOutputRows = proteinQuantificationMethod(peptQuantRows, params, proteinModifier, getEvalFeatures)
	  File "/usr/local/lib/python2.7/dist-packages/triqler/triqler.py", line 339, in getPickedProteinCalibration
		hyperparameters.fitPriors(peptQuantRows, params) # updates priors
	  File "/usr/local/lib/python2.7/dist-packages/triqler/hyperparameters.py", line 63, in fitPriors
		fitDist(protStdevsInGroup, funcGamma, "stdev log10(protein diff in group)", ["shapeInGroupStdevs", "scaleInGroupStdevs"], params, plot, x = np.arange(-0.1, 1.0, 0.005))
	  File "/usr/local/lib/python2.7/dist-packages/triqler/hyperparameters.py", line 110, in fitDist
		popt, _ = curve_fit(func, bins, vals)
	  File "/usr/local/lib/python2.7/dist-packages/scipy/optimize/minpack.py", line 710, in curve_fit
		ydata = np.asarray_chkfinite(ydata)
	  File "/usr/local/lib/python2.7/dist-packages/numpy/lib/function_base.py", line 461, in asarray_chkfinite
		"array must not contain infs or NaNs")
	ValueError: array must not contain infs or NaNs
	
2019-01-05
----
### 15:30
I have changed the knime pipeline to output idXML files, which are then used in a module I found called "ProteinQuantifier".
I'm running the workflow as I write this and has gotten some results with the CruxAdapter. The scan time used was from 3000 to 4200 in Msconvert

Data uploaded to results/2019-01-05_knime_results

However, I need some time to go through the data
