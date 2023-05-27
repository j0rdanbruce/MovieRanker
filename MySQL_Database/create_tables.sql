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

create table if not exists Movie(
	id int not null auto_increment unique,
    title varchar(70) not null,
    pic_url varchar(150),
    plot varchar(600),
    TMDB_id int not null unique,
    primary key(id)
);

create table if not exists Likes_Movie(
	user_id int not null,
	movie_id int not null,
	primary key(user_id, movie_id),
    foreign key(user_id) references user(id),
    foreign key(movie_id) references Movie(id)
);