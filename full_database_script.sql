create table partners
(
    id integer not null primary key,
    company_name varchar(255) not null,
    address varchar(255) not null,
    inn varchar(255) not null,
    last_name_director varchar(255) not null,
    first_name varchar(255) not null,
    patronymic varchar(255),
    phone_number varchar(255),
    email varchar(255),
    logo_path varchar(255) not null,
    rating varchar(255) not null,
    product_realisation varchar(255) not null
);

create table market_place
(
    id integer not null primary key,
    country varchar(255) not null,
    city varchar(255) not null,
    street varchar(255) not null,
    building_number integer not null
);

create table market_place_of_partners
(
    id integer not null primary key,
    id_market_place integer not null references market_place,
    id_partners integer not null references partners
);

create table manager
(
    id integer not null primary key,
    last_name_director varchar(255) not null,
    first_name varchar(255) not null,
    patronymic varchar(255)
);