CREATE TABLE `stock` (
  `id` tinyint(4) unsigned NOT NULL AUTO_INCREMENT,
  `ticker` char(5) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `exchange` varchar(8) DEFAULT NULL,
  `pv_close` int(11) DEFAULT NULL,
  `pv_volume` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `quote` (
  `id` tinyint(4) unsigned NOT NULL,
  `price` int(10) unsigned NOT NULL,
  `volume` int(10) unsigned NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`time`,`id`),
  KEY `id` (`id`),
  CONSTRAINT `stock_data_ibfk_1` FOREIGN KEY (`id`) REFERENCES `stock` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `portfolio` (
  `id` tinyint(4) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `init_fund` int(10) unsigned DEFAULT 10000000,
  `strategy` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `position` (
  `portfolio` tinyint(4) unsigned NOT NULL,
  `stock` tinyint(4) unsigned NOT NULL,
  `shares` int(10) NOT NULL,
  `avg_cost` int(10),
  `total_cost` int(10) NOT NULL,
  `aggr_cost` int(10),
  PRIMARY KEY (`portfolio`, `stock`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `transaction` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `portfolio` tinyint(4) unsigned NOT NULL,
  `stock` tinyint(4) unsigned NOT NULL,
  `action` char(5) NOT NULL,
  `shares` int(10) NOT NULL,
  `price` int(10) unsigned NOT NULL,
  `total` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
