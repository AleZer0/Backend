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
    ud.puesto,
    a.fecha,
    a.tipoAcceso
FROM `user_detail` ud
JOIN `user` u ON ud.idUser = u.idUser
JOIN `access` a ON ud.idUser = a.idUser
ORDER BY ud.idUser, a.fecha;

SELECT
	ud.idUser,
    a.fecha,
    a.tipoAcceso
FROM `user_detail` ud
JOIN `access` a ON ud.idUser = a.idUser
ORDER BY ud.idUser, a.fecha;

SELECT count(*) FROM access WHERE idUser = 13;
SELECT * FROM access WHERE idUser = 13 AND tipoAcceso = "Entrada";

INSERT INTO `accesos_xrom`.`user` (`nombre`, `apellido`) VALUES ("Alexis Balaam", "Díaz Rodríguez");
INSERT INTO `accesos_xrom`.`user_detail` (`idUser`, `nacimiento`, `puesto`) VALUES ('21', '2003-06-22 00:00:00', 'Junior');

DELETE ud, u
FROM `user_detail` ud
JOIN `user` u ON ud.idUser = u.idUser
WHERE ud.idUser = 20;

SELECT GROUP_CONCAT(COLUMN_NAME) AS columnas
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'checador_xrom' 
AND TABLE_NAME = 'user_detail';
