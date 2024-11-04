@echo off
setlocal EnableDelayedExpansion

set "input_names_file=config/input_names.txt"
set "output_name=AMVR_Tracking_GielenLars_PexJan-Mathijs_RoosenVinz"
set "temp_dir=build\temp"

rem Create a temp directory if it doesn't exist
if not exist "%temp_dir%" ( mkdir "%temp_dir%" )

rem Replace 'images/' with 'source/images/'
for /F "tokens=*" %%i in (%input_names_file%) do ( powershell -Command "(Get-Content 'source\%%i') -replace '^!\[(.*)\]\(images/(.*)\)', '^![$1](source/images/$2)' | Set-Content '%temp_dir%\%%i'" )

@REM rem Initialize the command with basic options
set "pandoc_cmd=pandoc -o build/%output_name%.pdf --filter pandoc-crossref --bibliography=source/references.bib --csl=config/bibliography.csl --template=config/eisvogel.latex --listings --number-sections -s -f markdown"

@REM Add files to include
for /F "tokens=*" %%i in (%input_names_file%) do ( set "pandoc_cmd=!pandoc_cmd! %temp_dir%/%%i" )
set "pandoc_cmd=!pandoc_cmd! config/metadata.yaml"

@REM REM Run the command
!pandoc_cmd!

endlocal