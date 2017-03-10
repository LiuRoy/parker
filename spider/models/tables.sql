CREATE SCHEMA `parker` DEFAULT CHARACTER SET utf8mb4 ;

CREATE TABLE `format` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `video_id` int(11) NOT NULL COMMENT '视频id',
  `video_url` varchar(200) NOT NULL COMMENT '播放url',
  `format` varchar(10) NOT NULL COMMENT '视频编码格式',
  `container` varchar(10) NOT NULL COMMENT 'flv/avi/mp4',
  `profile` varchar(10) NOT NULL COMMENT '1080P/高清',
  `size` int(11) NOT NULL DEFAULT '0' COMMENT '视频大小',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否下载完成 1下载完成 0未下载',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_video_id` (`video_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='视频格式表'

CREATE TABLE `videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `publisher` varchar(20) NOT NULL DEFAULT '' COMMENT '发布人名称',
  `source` varchar(10) NOT NULL COMMENT '网站类型',
  `task_id` int(11) NOT NULL COMMENT '任务id',
  `comment_count` int(11) NOT NULL DEFAULT '0' COMMENT '评论个数',
  `star_count` int(11) NOT NULL DEFAULT '0' COMMENT '点赞个数',
  `play_count` int(11) NOT NULL DEFAULT '0' COMMENT '播放次数',
  `img_url` varchar(200) NOT NULL COMMENT '视频封面链接',
  `duration` int(11) NOT NULL COMMENT '视频时长',
  `title` varchar(200) NOT NULL DEFAULT '' COMMENT '视频标题',
  `publish_date` timestamp NULL DEFAULT NULL COMMENT '发布时间',
  `video_url` varchar(200) NOT NULL COMMENT '视频播放页面',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_video_url` (`video_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='视频信息表'