gcc_version=$(gcc -dumpversion)
gcc_name="gcc$gcc_version"
echo "GCC version = $gcc_name"
find ../lib -name '*gcc*' -exec bash -c ' gcc_name="gcc$(gcc -dumpversion)"; mv $0 ${0/gcc/$gcc_name}' {} \;

