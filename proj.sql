create database project;
use project;

create table AdminLogin(username varchar(250),password varchar(250));
Insert into adminlogin values('Gourav','Hello');
select * from adminlogin;

create table AdminLoggedin(IP varchar(200));
select * from AdminLoggedin;

create table UserInfo(id int,firstname varchar(150),lastname varchar(150),dob date,address varchar(150),phone_number varchar(10),dept varchar(200),year varchar(5),rank_ int,primary key(id));
create table UserLogin(id int,username varchar(150) unique,password varchar(150));
create table UserLoggedIn(IP varchar(200),id int);
select * from UserInfo;

create table elections_current(eid int,description varchar(300),start_time datetime,end_time datetime,dept varchar(200),year varchar(5),rank_ int,primary key(eid));
create table votes(eid int,id int,cid int);
create table elections_history(eid int,description varchar(100),winner varchar(100),start_time datetime,end_time datetime,dept varchar(200),year varchar(5),rank_ int);
create table candidates(eid int,cid int,cname varchar(100),description varchar(1000),foreign key(eid) references elections_current(eid));
select * from votes;
