PGPASSFILE='/Users/.pgpass'

## run the downloader

python gaabsenteefiledown.py

## adding time for download to complete, it's a large file

sleep 120

## unzip the file into the folder

7z x /Users/michaelwood/Documents/35213.zip

## first section cleans up the header for special characters and spaces
## second removes weird space that causes an error in the upload 

head -1 STATEWIDE.csv  | sed -e 's/#/num/g' -e 's/\///g'  -e 's/ /_/g' > MINISTATEWIDE.csv
tail -n +2 STATEWIDE.csv | awk -F, -v OFS="," '{gsub(/ /,"",$9)}1' >>  MINISTATEWIDE.csv


## truncate the table and write the csv to the postgres instance

psql  -c "truncate table gendata.ga_absentee;" 

psql -c "\copy gendata.ga_absentee FROM '/Users/michaelwood/Documents/GenerationData/Scripts/MINISTATEWIDE.csv' DELIMITER ',' NULL '' CSV HEADER;"

## write out qc checks

psql "select count(*)
, count(case when ballot_return_date is not null then 1 else null end) as ballots_returned
, count(case when ballot_return_date > current_date - 1  then 1 else null end) as ballots_returned_yesterday
from gendata.ga_absentee;"> data.txt


# print results to terminal

cat data.txt

## remove all the folders and the parent

find . -name "*.csv" -type f -delete

rm /Users//Documents/35213.zip