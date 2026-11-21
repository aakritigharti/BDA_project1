create schema if not exists student_project;

create table if not exists student_project.books (
book_key VARCHAR(100) PRIMARY KEY,
title TEXT,
authors TEXT,
first_publication_year INTEGER,
subjects TEXT,
isbn TEXT,
languages TEXT,
publishers TEXT,
total_editions INTEGER,
cover_id BIGINT,
publication_dates TEXT,
primary_author TEXT,
primary_subject TEXT,
author_count INTEGER,
subject_count INTEGER,
cover_url TEXT);

select * from student_project.books;

select table_name
from information_schema.tables
where table_schema = 'student_project';

select count(*) AS total_books
from student_project.books;

select count(*) AS total_books,
count(*) filter (where title is null) AS missing_titles, 
count(*) filter (where authors is null) AS missing_authors,
count(*) filter (where isbn is null) AS missing_isbn,
count(*) filter (where cover_id is null) AS missing_covers
from student_project.books;

--books by publication year--
select first_publication_year, count(*) AS total_books
from student_project.books
where first_publication_year is not null
group by first_publication_year
order by first_publication_year;

--top 10 primary authors with there books
select primary_author, count(*) AS total_books
from student_project.books
group by primary_author
order by total_books DESC
limit 10;

--first 20 books
select book_key, title, primary_author, first_publication_year, total_editions
from student_project.books
limit 20;

--distinct count of books
select count(distinct title) from student_project.books;

--count of books
select count(title) from student_project.books;

--count of distinct authors
select count(distinct primary_author) AS total_unique_authors
from student_project.books;

--count of distinct authors where author is unknown
select count(distinct primary_author) AS total_unique_authors
from student_project.books
where primary_author is not null and primary_author ='Unknown';

--no. of books published after 2015
select title, primary_author, first_publication_year
from student_project.books
where first_publication_year > 2015
order by first_publication_year desc;

--books with more than 10 editions
select title, primary_author, total_editions
from student_project.books
where total_editions > 10
order by total_editions DESC;

--books with available cover url
select title,cover_id,cover_url
from student_project.books
where cover_id is not null;

--books published with each year
select first_publication_year,count(*) AS total_books
from student_project.books
where first_publication_year is not null
group by first_publication_year
order by first_publication_year;

--no.of books with different languages
select languages,count(*) AS total_books
from student_project.books
group by languages
order by total_books DESC
limit 10;

--average no.of editions per books
select avg(total_editions) AS average_editions,
max(total_editions) AS maximum_editions,
min(total_editions) AS minimum_editions
from student_project.books
where total_editions is not null;

--authors more than two books
select primary_author,count(*) AS total_books
from student_project.books
where primary_author is not null and primary_author = 'Unknown'
group by primary_author
having count(*) > 2
order by total_books DESC;

--no.of books by certain period of published years
select
    case
        when  first_publication_year < 1950
            then 'Before 1950'
        when first_publication_year between 1950 and 1999
            then '1950-1999'
        when first_publication_year between 2000 and 2009
            then '2000-2009'
        when first_publication_year between 2010 and 2019
            then '2010-2019'
        when first_publication_year >= 2020
            then '2020 onwards'
        else 'Unknown'
    end as publication_period,
    count(*) AS total_books
from student_project.books
group by publication_period
order by total_books DESC;

--no.of books based on editions count
select
    case
        when total_editions = 1 then 'Single Edition'
        when total_editions between 2 and 5 then '2-5 Editions'
        when total_editions between 6 and 10 then '6-10 Editions'
        when total_editions > 10 then 'More than 10 Editions'
        else 'Unknown'
    end as edition_category,
    count(*) AS total_books
from student_project.books
group by edition_category
order by total_books DESC;

--no.of books with editions more than average
with average_edition AS (
    select avg(total_editions) AS avg_editions
    from student_project.books
)
select title,primary_author,total_editions
from student_project.books
where total_editions > (
    select avg_editions
    from average_edition
)
order by total_editions DESC;

--book with recent published year
select title,primary_author,first_publication_year
from student_project.books
where first_publication_year = (
    select MAX(first_publication_year)
    from student_project.books
)
and first_publication_year is not null;

--ranking the no.of authors based on no.of books
with author_counts AS (
    select primary_author,count(*) AS total_books
    from student_project.books
    group by primary_author
)
select primary_author, total_books,
rank() over (
        order by total_books DESC
    ) AS author_rank
from author_counts
order by author_rank;

--cumulative books by publication year
with yearly_books AS (
    select first_publication_year,count (*) AS total_books
    from student_project.books
    where first_publication_year is not null
    group by first_publication_year
)
select first_publication_year, total_books,
    sum(total_books) over (
        order by first_publication_year
    ) AS cumulative_books
from yearly_books
order by first_publication_year;

--no.of books with most authors
select title,authors,author_count
from student_project.books
order by author_count desc;

--no.of books with most subjects
select title,subjects,subject_count
from student_project.books
order by subject_count DESC
limit 10;



--creating new table for the joins practise
create table if not exists student_project.authors (
    author_id SERIAL PRIMARY KEY,
    author_name TEXT UNIQUE NOT NULL
);

--inserting unique value in authors table by existing book table
insert into student_project.authors (author_name)
select distinct primary_author
from student_project.books
where primary_author is not null 
on conflict (author_name) do nothing;

select * from student_project.authors;

--creating new table for the join practise
create table if not exists student_project.subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name TEXT UNIQUE NOT NULL
);

--inserting unique value in subjects by exisitng book table
insert into student_project.subjects (subject_name)
select distinct primary_subject
from student_project.books
where primary_subject is not null
on conflict (subject_name) do nothing;

select * from student_project.subjects;

--inner joins of books with their subjects
select b.title,b.primary_subject,s.subject_id,s.subject_name
from student_project.books b
inner join student_project.subjects s
on b.primary_subject = s.subject_name;

--inner joins no.of books with respective authors
select a.author_name,count(b.book_key) AS total_books
from student_project.authors a
inner join student_project.books b
    on a.author_name = b.primary_author
group by a.author_name
order by total_books desc;

--multiple joins on books,authors,subjects
select b.title,a.author_name,s.subject_name,b.first_publication_year,b.total_editions
from student_project.books b
inner join student_project.authors a
    on b.primary_author = a.author_name
inner join student_project.subjects s
    on b.primary_subject = s.subject_name
order by b.title;