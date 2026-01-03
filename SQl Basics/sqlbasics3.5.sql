select * from movies where imdb_rating > 9;
select * from movies where imdb_rating between 6 and 8;
select * from movies where release_year in ( 2022 ,2018);
select * from movies where imdb_rating is null;
select * from movies where industry = "Bollywood" order by imdb_rating desc;
select * from movies where industry = "Hollywood" order by imdb_rating desc limit 5;
select * from movies where industry = "Hollywood" order by imdb_rating desc limit 5 offset 1;

