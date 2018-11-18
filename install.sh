PLUGIN_DIRECTORY=~/.kicad/scripting/plugins
CURRENT_DIRECTORY=$(pwd)

if [ ! -d "$PLUGIN_DIRECTORY" ]; then
	echo "Couldn't find plugin directory, creating now"
	mkdir -p $PLUGIN_DIRECTORY
fi
copy_file() {
echo "Copying $1"
cp $1 $PLUGIN_DIRECTORY
}
for file in $CURRENT_DIRECTORY/*.py
do
copy_file "$file"
done
