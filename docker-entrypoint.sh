echo "\n\033[0;32mPackage Installation started (Please wait for 2 minutes)...\033[0m"
if poetry lock > /dev/null 2> error.log && poetry install --with dev > /dev/null 2>> error.log
then
    echo "\n\033[0;32mInstallation completed successfully.\033[0m"
else
    echo "\n\033[0;31mInstallation failed. See error.log for details.\n\nerror.log:\033[0m"
    cat error.log
	exit 1
fi

echo "\033[0;36m\n\nHelp Manual for 'poetry run main' command\033[0m\n"
poetry run main --help

if [ -f setup/.env ]; then
  export $(cat setup/.env | sed 's/#.*//g' | xargs)
fi

exec bash
