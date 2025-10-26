echo "Moving to $1"
sleep 0.1
cd $1

echo "Clearing compiled/"
sleep 0.1
cd compiled/
rm *.html
echo "compiled/ cleared. I hope you didn't put anything important in there!"

echo "\nRunning make script.\n"
sleep 0.1
cd ../../
python3 compilepages.py $1

echo "\n"

if [ ${2:+1} ]; then
    cd "$1/assignments/"
    echo "Running LaTeX compiler on $2...\n"
    pdflatex -interaction=batchmode $2.tex
    echo "\nRunning biber compiler on $2...\n"
    biber -q $2
    echo "\nRunning LaTeX compiler on $2 again...\n"
    pdflatex -interaction=batchmode $2.tex

    echo "\nCleaning up assignments/"
    echo ls
    rm *.aux
    rm *.bcf
    rm *.fdb_latexmk
    rm *.fls
    rm *.idx
    rm *.ilg
    rm *.ind
    rm *.log
    rm *.out
    rm *.xml
    rm *.gz
    echo "\n"
fi
