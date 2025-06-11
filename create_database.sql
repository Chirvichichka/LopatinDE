create table material_types
(
    id   INTEGER not null
        primary key,
    name VARCHAR not null
);

create table materials
(
    id               INTEGER not null
        primary key,
    type_id          INTEGER
        references material_types,
    name             VARCHAR not null
        unique,
    price            FLOAT,
    unit             VARCHAR,
    package_quantity FLOAT,
    stock_quantity   FLOAT,
    min_quantity     FLOAT
);

create table product_types
(
    id          INTEGER not null
        primary key,
    name        VARCHAR not null,
    coefficient FLOAT   not null
);

create table products
(
    id                INTEGER not null
        primary key,
    type_id           INTEGER
        references product_types,
    name              VARCHAR not null,
    article           VARCHAR not null
        unique,
    min_partner_price FLOAT,
    quantity          FLOAT
);

create table material_product
(
    material_id INTEGER
        references materials,
    product_id  INTEGER
        references products,
    quantity    FLOAT
);

