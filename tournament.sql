-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- drop database tournament;

create database tournament;

\c tournament;

create table players(id serial, name varchar(50) not null, matches integer default 0, wins integer default 0, constraint players_pk primary key(id));

create table matches(id serial primary key, winner integer references players(id) on delete cascade, loser integer references players(id) on delete cascade);

