CREATE SCHEMA `parker` DEFAULT CHARACTER SET utf8mb4 ;

CREATE TABLE `download_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `video_id` int(11) NOT NULL COMMENT '视频id',
  `video_url` varchar(200) NOT NULL COMMENT '播放url',
  `video_title` varchar(200) NOT NULL COMMENT '视频标题',
  `video_size` int(11) NOT NULL DEFAULT '0' COMMENT '视频大小',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否下载完成 1下载完成 0未下载',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_video_id` (`video_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='视频下载信息表';

CREATE TABLE `web_video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` varchar(10) NOT NULL COMMENT '网站类型',
  `task_id` int(11) NOT NULL COMMENT '任务id',
  `img_url` varchar(200) NOT NULL COMMENT '视频封面链接',
  `duration` int(11) NOT NULL COMMENT '视频时长',
  `title` varchar(200) NOT NULL DEFAULT '' COMMENT '视频标题',
  `video_url` varchar(200) NOT NULL COMMENT '视频播放页面',
  `video_url_md5` varchar(32) NOT NULL COMMENT '视频播放页面',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_video_url_md5` (`video_url_md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='网站视频信息';
