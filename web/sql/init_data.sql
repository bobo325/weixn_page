-- 初始化数据脚本 以行为单位读取执行  一条语句写位一行
INSERT INTO `media_conf` (`id`, `type_name`, `format`, `limit_size`, `create_time`, `update_time`) VALUES ('1', 'image', 'jpg,png', '3145728', '2018-01-10 00:00:00', '2018-02-01 09:50:39');
INSERT INTO `media_conf` (`id`, `type_name`, `format`, `limit_size`, `create_time`, `update_time`) VALUES ('2', 'audio', 'mp3,wma,m4a', '20971520', '2018-01-10 00:00:00', NULL);
INSERT INTO `media_conf` (`id`, `type_name`, `format`, `limit_size`, `create_time`, `update_time`) VALUES ('3', 'video', 'mp4,flv', '104857600', '2018-01-10 00:00:00', NULL);
INSERT INTO `media_conf` (`id`, `type_name`, `format`, `limit_size`, `create_time`, `update_time`) VALUES ('4', 'doc', 'doc,xls,ppt,pdf,docx', '104857600', '2018-01-10 00:00:00', NULL);
INSERT INTO `media_conf` (`id`, `type_name`, `format`, `limit_size`, `create_time`, `update_time`) VALUES ('5', 'zip', 'zip,rar', '104857600', '2018-01-10 00:00:00', NULL);
INSERT INTO `media_conf` (`id`, `type_name`, `format`, `limit_size`, `create_time`, `update_time`) VALUES ('6', 'other', '7z', '104857600', '2018-01-10 00:00:00', NULL);


INSERT INTO `metadata` (`id`, `name`, `version`, `company`, `logo`, `favicon`, `lock_user_threshold`, `captcha_threshold`, `create_time`, `modify_time`) VALUES ('1', '通用型后台管理系统', '1.0.0', '江西有路科技有限公司', '/static_file/system_logo.png', '/static_file/system_favicon.ico', '5', '3', '2018-01-23 10:59:44', '2018-01-23 10:59:44');

INSERT INTO `organization` (`id`, `name`, `pid`, `enable`, `description`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('1', '全国', '0', '1', '根节点', '0', '2018-01-09 14:07:10', '0', '2018-01-09 14:07:19');

-- 初始化权限
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('1', '添加', '组织架构', '/org/add', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('2', '修改', '组织架构', '/org/update', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('3', '查询', '组织架构', '/org/list', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('4', '删除', '组织架构', '/org/delete', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('5', '启用', '组织架构', '/org/enable', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('6', '禁用', '组织架构', '/org/disable', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('7', '添加', '用户管理', '/user/add', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('8', '修改', '用户管理', '/user/update', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('9', '个人中心重置密码', '用户管理', '/user/resetpwd', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('10', '个人中心查询', '用户管理', '/user/personal', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('11', '个人中心修改', '用户管理', '/user/personal_update', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('12', '管理员直接设置密码', '用户管理', '/user/modifypwd', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('13', '查询', '用户管理', '/user/list', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('14', '删除', '用户管理', '/user/delete', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('15', '启用', '用户管理', '/user/enable', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('16', '禁用', '用户管理', '/user/disable', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('17', '登录', '用户管理', '/user/login', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('18', '注销', '用户管理', '/user/logout', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('19', '查询', '权限管理', '/auth/list', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('20', '启用', '权限管理', '/auth/enable', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('21', '禁用', '权限管理', '/auth/disable', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('22', '审核', '权限管理', '/auth/audit', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('23', '添加', '角色管理', '/role/add', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('24', '修改', '角色管理', '/role/update', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('25', '查询', '角色管理', '/role/list', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('26', '删除', '角色管理', '/role/delete', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('27', '设置权限', '角色管理', '/role/set_auth', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('28', '启用', '角色管理', '/role/enable', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('29', '禁用', '角色管理', '/role/disable', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('30', '查询', '操作日志', '/opr/list', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('31', '基本设置修改', '系统设置', '/metadata/update', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('32', '查询', '系统设置', '/metadata/list', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('33', '添加', '发件箱', '/message/outbox/add', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('34', '查询', '发件箱', '/message/outbox/list', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('35', '删除', '发件箱', '/message/outbox/delete', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('36', '消息详情', '发件箱', '/message/outbox/detail', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('37', '上传', '媒体库', '/media/upload', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('38', '删除', '媒体库', '/media/delete', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('39', '查询', '媒体库', '/media/list', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('40', '详情', '媒体库', '/media/detail', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('41', '编辑', '媒体库', '/media/update', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('42', '生成缩略图', '媒体库', '/media/thumbnail', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('43', '类型查询', '媒体库', '/mediaType/list', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('44', '类型编辑', '媒体库', '/mediaType/update', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('45', '查询', '收件箱', '/message/inbox/list', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('46', '删除', '收件箱', '/message/inbox/delete', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('47', '消息详情', '收件箱', '/message/inbox/detail', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('48', '标记为已读', '收件箱', '/message/inbox/read', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('49', '删除', '站内信', '/message/manage/delete', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('50', '查询', '站内信', '/message/manage/list', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');
INSERT INTO `auth` (`id`, `name`, `module`, `opr_url`, `need_auditing`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('51', '消息详情', '站内信', '/message/manage/detail', '1', '1', '1', '2018-02-28 09:16:31', '1', '2018-03-07 11:11:59');

-- 初始化角色
INSERT INTO `role` (`id`, `name`, `description`, `enable`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('1', 'root', '超级管理员', '1', '1', '2018-01-09 16:39:38', NULL, NULL);

--  初始化管理员权限
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('1', '1', '1');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('2', '1', '2');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('3', '1', '3');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('4', '1', '4');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('5', '1', '5');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('6', '1', '6');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('7', '1', '7');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('8', '1', '8');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('9', '1', '9');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('10', '1', '10');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('11', '1', '11');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('12', '1', '12');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('13', '1', '13');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('14', '1', '14');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('15', '1', '15');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('16', '1', '16');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('17', '1', '17');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('18', '1', '18');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('19', '1', '19');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('20', '1', '20');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('21', '1', '21');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('22', '1', '22');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('23', '1', '23');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('24', '1', '24');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('25', '1', '25');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('26', '1', '26');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('27', '1', '27');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('28', '1', '28');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('29', '1', '29');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('30', '1', '30');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('31', '1', '31');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('32', '1', '32');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('33', '1', '33');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('34', '1', '34');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('35', '1', '35');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('36', '1', '36');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('37', '1', '37');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('38', '1', '38');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('39', '1', '39');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('40', '1', '40');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('41', '1', '41');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('42', '1', '42');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('43', '1', '43');
INSERT INTO `role_auth` (`id`, `role_id`, `auth_id`) VALUES ('44', '1', '44');

-- 初始化管理员账户
INSERT INTO `user` (`id`, `org_id`, `role_id`, `username`, `password`, `real_name`, `email`, `tel`, `profile_photo`, `login_error_num`, `enable`, `description`, `last_login_time`, `creator`, `create_time`, `updator`, `update_time`) VALUES ('1', '1', '1', 'admin', 'c56d0e9a7ccec67b4ea131655038d604', '超级管理员', '', '', '', '0', '1', '超级管理员', NULL, '1','2018-01-09 17:21:55', '1', '2018-01-09 17:21:55');
