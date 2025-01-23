SELECT
	ud.idUser,
    u.nombre,
    u.apellido,
    ud.foto,
    ud.puesto
FROM `user_detail` ud
JOIN `user` u ON ud.idUser = u.idUser
ORDER BY ud.idUser;

SELECT
	ud.idUser,
    u.nombre,
    u.apellido,
    ud.foto,
    ud.puesto
FROM `user_detail` ud
JOIN `user` u ON ud.idUser = u.idUser
ORDER BY ud.idUser;

SELECT * FROM `user`;

SELECT
	ud.idUser,
	u.nombre,
	u.apellido,
	ud.puesto,
	ud.foto,
	a.fecha,
	a.tipoAcceso,
	WEEK(a.fecha, 1) AS semana
FROM `user_detail` ud
JOIN `user` u ON ud.idUser = u.idUser
JOIN `access` a ON ud.idUser = a.idUser
WHERE WEEK(a.fecha, 1) = 53
ORDER BY ud.idUser, a.fecha;

SELECT
	`idUser`,
    `fecha`,
    `tipoAcceso`,
    WEEK(`fecha`, 1) AS semana
FROM `access` WHERE `idUser` = 13 AND WEEK(`fecha`, 1) = 53;

SELECT count(*) FROM access WHERE idUser = 13;
SELECT * FROM access WHERE idUser = 13 AND tipoAcceso = "Entrada";

INSERT INTO `accesos_xrom`.`user` (`nombre`, `apellido`) VALUES ("Alexis Balaam", "Díaz Rodríguez");
INSERT INTO `accesos_xrom`.`user_detail` (`idUser`, `nacimiento`, `puesto`) VALUES ('21', '2003-06-22 00:00:00', 'Junior');

DELETE ud, u
FROM `user_detail` ud
JOIN `user` u ON ud.idUser = u.idUser
WHERE ud.idUser = 20;

SELECT COLUMN_NAME AS columnas
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'accesos_xrom' 
AND TABLE_NAME = 'user_detail';

SELECT `idUser` FROM `user` ORDER BY `idUser` DESC LIMIT 1;
delete from `user` where `idUser` = 24;
