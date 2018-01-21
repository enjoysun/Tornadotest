drop database house;
create database house charset=utf8;
use house;
create table tb_user_info(
	user_id bigint auto_increment comment '用户id',
	user_name varchar(64) not null comment '用户姓名',
	user_gender tinyint not null default 0 comment '用户性别默认0',
	user_age int null comment '年龄',
	user_mobile char(11) not null comment '手机号',
	user_img varchar(128) null comment '头像',
	user_passwd varchar(128) not null comment '密码',
	user_ctime datetime default current_timestamp comment '创建时间',
	user_utime datetime default current_timestamp on update current_timestamp comment '更新时间',
	primary key (user_id),
	unique (user_mobile) # 指定唯一，unique也做了 key (user_mobile)操作
) engine=InnoDB default charset=utf8 comment '用户表';

create table tb_house_info(
	house_id bigint auto_increment comment '房屋id',
	house_user_id bigint not null comment '用户id',
	house_name varchar(128) not null comment '房屋名',
	house_address varchar(256) not null comment '地址',
	house_price int not null comment '价钱',
	house_description varchar(500) null comment '描述',
	house_ctime datetime not null default current_timestamp comment'插入时间',
	house_utime datetime not null default current_timestamp on update current_timestamp comment'更新时间',
	primary key (house_id),
	constraint foreign key (house_user_id) references tb_user_info(user_id)
) engine=InnoDB default charset=utf8 comment'房屋表';

create table tb_img_info(
	img_id bigint auto_increment comment'图片id',
	img_house_id bigint not null comment'房屋id',
	img_url varchar(128) null comment'',
	img_ctime datetime not null default current_timestamp comment'',
	img_utime datetime not null default current_timestamp on update current_timestamp,
	primary key (img_id),
	constraint foreign key (img_house_id) references tb_house_info(house_id)
)engine=InnoDB default charset=utf8 comment'图片表';