DELIMITER //

CREATE PROCEDURE CalcularSuma(IN nombre1 varchar(20), IN nombre2 varchar(20), OUT resultado int)
BEGIN
    DECLARE longitud int;
    DECLARE contador int;
    DECLARE caracter varchar(1);
    DECLARE sql_stmt varchar(2000);
    DECLARE columna varchar(2);
    DECLARE apoyo varchar(20);

    -- Crear la tabla "nombre"
    SET sql_stmt = 'CREATE TABLE nombre (';
    SET longitud = CHAR_LENGTH(nombre1);
    SET contador = 1;

    WHILE contador <= longitud DO
        SET caracter = SUBSTRING(nombre1, contador, 1);
        SET columna = CONCAT(caracter, contador);
        SET sql_stmt = CONCAT(sql_stmt, columna, ' INT,');
        SET contador = contador + 1;
    END WHILE;

    SET sql_stmt = LEFT(sql_stmt, CHAR_LENGTH(sql_stmt) - 1);
    SET sql_stmt = CONCAT(sql_stmt, ');');
    PREPARE stmt FROM sql_stmt;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    -- Insertar valores en la tabla "nombre" según nombre2
    SET longitud = CHAR_LENGTH(nombre2);
    SET contador = 1;

    WHILE contador <= longitud DO
        SET caracter = SUBSTRING(nombre2, contador, 1);

        SELECT COLUMN_NAME INTO columna
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'nombre'
        AND ORDINAL_POSITION = contador
        AND LEFT(COLUMN_NAME, 1) = caracter
        ORDER BY ORDINAL_POSITION
        LIMIT 1;

        SET sql_stmt = CONCAT('INSERT INTO nombre(', columna, ') VALUES (1);');
        PREPARE stmt FROM sql_stmt;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

        SET contador = contador + 1;
    END WHILE;

    -- Calcular la suma de cada columna de la tabla "nombre"
    SET sql_stmt = '';
    SET contador = 1;

    WHILE contador <= longitud DO
        SELECT CONCAT('SUM(IFNULL(', COLUMN_NAME, ', 0))+') INTO apoyo
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'nombre'
        AND ORDINAL_POSITION = contador;

        SET sql_stmt = CONCAT(sql_stmt, apoyo);
        SET contador = contador + 1;
    END WHILE;

    SET sql_stmt = LEFT(sql_stmt, CHAR_LENGTH(sql_stmt) - 1);
    SET sql_stmt = CONCAT('SELECT ', sql_stmt, ' INTO @resultado FROM nombre;');
    PREPARE stmt FROM sql_stmt;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    SET resultado = @resultado;
END //

DELIMITER ;

SET @nombre1 = 'MARTHA';
SET @nombre2 = 'MARTA';
SET @resultado = 0;

CALL CalcularSuma(@nombre1, @nombre2, @resultado);

SELECT @resultado;
