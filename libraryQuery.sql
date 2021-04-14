create table users (
	user_id serial primary key,
	username varchar,
	name varchar,
	password varchar, 
	email varchar unique
);

drop table users;

create table book (
	book_id serial primary key,
	title varchar,
	author varchar,
	stock integer
);

drop table book;

create table transactions (
	transaction_id serial primary key,
	user_id integer,
		foreign key (user_id)
		references users(user_id),
	book_id integer,
		foreign key (book_id)
		references book(book_id),
	checkout_date timestamp,
	return_date timestamp
);

drop table transactions;

insert into
book(title, stock, author)
values
('Hamlet', '3', 'William Shakespearse'),
('Don Quixote', '3', 'Miguel de Cervantes'),
('A Tale of Two Cities', '4', 'Charles Dickens'),
('Treasure Island', '4', 'R. L. Stevenson'),
('Pride and Prejudice','5', 'Jane Austen')
;
