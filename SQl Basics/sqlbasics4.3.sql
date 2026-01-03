select  movies.*,languages.name from movies left outer join languages using(language_id);
select  movies.* from movies left outer join languages using(language_id) where languages.name = "Telugu";

select  languages.name,count(*) from movies left outer join languages using(language_id) group by languages.name;




