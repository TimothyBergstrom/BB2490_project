read -p "Choose directory: " dir
current_dir=$(pwd)
choosen_dir="$current_dir/$dir"
cd "$choosen_dir"
ls -R | grep "\.mzML$"
ls -R | grep "\.mzML$" | awk -v choosen_dir="$choosen_dir" '{print $1}' > "$current_dir/batch_list.txt"
cd "$current_dir"
