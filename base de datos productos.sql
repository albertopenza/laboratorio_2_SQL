CREATE DATABASE Productos_db;
use Productos_db;
create table producto (
id_productos char (8) primary key ,
nombre varchar (50) not null ,
marca varchar (50) not null ,
precio decimal (10,2) not null,
stock int not null ,
garantia int not null
);
create table productoTelevisor (
id_productos char(8) primary key ,
pantalla_pulgadas int not null ,
foreign key (id_productos) references producto (id_productos) 
);
create table productoHeladera (
id_productos char(8) primary key ,
capacidad_litros int not null ,
foreign key (id_productos) references producto (id_productos) 
);
use productos ;


