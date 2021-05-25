create table Plot(
plotid int not null,
projectid int not null,
plotNo varchar(30) not null,
Area int not null,
rate int,
constraint pk_plots primary key (plotno),
UNIQUE(projectid, plotNo)
);

create table Dealer(
dealerID int auto_increment not null,
dealerName varchar(50),
phone varchar(15),
primary key (dealerId)
);

create table deals(
deal_id int not null,
plotno int not null,
dealerId int,
customerName int not null
);

create table Customer(
customerid int auto_increment,   not important to save
customerName varchar(50), 
phone varchar(15) not null,
constraint pk_customer primary key (customerid)
);