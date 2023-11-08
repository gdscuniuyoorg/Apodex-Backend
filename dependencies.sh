while read -r line; do
    package=$(echo $line | cut -d'=' -f1)
    pip uninstall -y $package
done < installed.txt
