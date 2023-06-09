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
	id int not null unique,
    title varchar(70) not null,
    pic_url varchar(150),
    plot varchar(600),
    primary key(id)
);

create table if not exists Likes_Movie(
	user_id int not null,
	movie_id int not null,
	primary key(user_id, movie_id),
    foreign key(user_id) references user(id),
    foreign key(movie_id) references Movie(id)
);

create table if not exists Forum(
	id int not null unique auto_increment,
    title varchar(80) not null,
    body varchar(400) not null,
    upvote int not null default(0),
    downvote int not null default(0),
    owner int not null,
    primary key(id),
    foreign key(owner) references user(id)
);
alter table Forum add column private boolean default(false);
alter table Forum add column created datetime default(current_timestamp());
alter table Forum add column modified datetime default(current_timestamp());

create table if not exists Comment(
	id int not null unique auto_increment,
    body varchar(400) not null,
    likes int not null default(0),
    dislikes int not null default(0),
    owner int not null,
    forum_id int not null,
    primary key(id),
    foreign key(owner) references user(id),
    foreign key(forum_id) references Forum(id)
);
alter table Comment add column created datetime default(current_timestamp());
alter table Comment add column modified datetime default(current_timestamp());