create table if not exists user(
	id int not null auto_increment unique,
    fname varchar(50) not null,
    lname varchar(50) not null,
    username varchar(50) unique,
    email varchar(80) not null,
    pwrd_hash varchar(150) not null unique,
    created timestamp default current_timestamp,
    modified timestamp default current_timestamp,
    primary key(id)
);