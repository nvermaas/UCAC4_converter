# UCAC4 Converter

Convert UCAC4 catalog from ASCII to a SQL database. Options are:
  * mysqlite
  * postgres
  * mysql

The UCAC4 catalog contains stars up to magnitude 16 and is provided as a ASCII file.
The catalog can be downloaded from cds: 
  * http://cdsarc.u-strasbg.fr/viz-bin/Cat?I/322A

The ASCII format is described here:
  * https://irsa.ipac.caltech.edu/data/UCAC4/ucac4.html
  * https://irsa.ipac.caltech.edu/data/UCAC4/readme_u4.txt



## build
> build.sh

copy ucac4-convert-1.0.0.tar.gz to a repository

## deploy
> pip install https://uilennest.net/repository/ucac4-convert-1.0.0.tar.gz --upgrade

## Run
> ucac4-convert -h
>
> ucac4-convert --source_file=ucac4.txt --target ucac4.sqlite3

