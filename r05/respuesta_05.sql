CREATE FUNCTION CalcularSuma(@nombre1 varchar(20), @nombre2 varchar(20))
RETURNS int
AS
BEGIN
    DECLARE @longitud int,
            @contador int,
            @caracter varchar(1),
            @sql nvarchar(2000),
            @columna varchar(2),
            @apoyo varchar(20),
            @resultado int

    -- Crear la tabla "nombre"
    SET @sql = 'CREATE TABLE nombre ('
    SET @longitud = LEN(@nombre1)
    SET @contador = 1

    WHILE @contador <= @longitud
    BEGIN
        SET @caracter = SUBSTRING(@nombre1, @contador, 1)
        SET @columna = CONCAT(@caracter, @contador)
        SET @sql = CONCAT(@sql, @columna, ' int,')
        SET @contador = @contador + 1
    END

    SET @sql = LEFT(@sql, LEN(@sql)-1)
    SET @sql = CONCAT(@sql, ')')
    EXEC sp_executesql @sql

    -- Insertar valores en la tabla "nombre" según @nombre2
    SET @longitud = LEN(@nombre2)
    SET @contador = 1

    WHILE @contador <= @longitud
    BEGIN
        SET @caracter = SUBSTRING(@nombre2, @contador, 1)

        SELECT top 1 @columna = COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'nombre'
        AND ORDINAL_POSITION = @contador
        AND LEFT(COLUMN_NAME, 1) = @caracter
        ORDER BY ordinal_position

        SET @sql = CONCAT('INSERT INTO nombre(', @columna, ') VALUES (1)')
        EXEC sp_executesql @sql

        SET @contador = @contador + 1
    END

    -- Calcular la suma de cada columna de la tabla "nombre"
    SET @sql = ''
    SET @contador = 1

    WHILE @contador <= @longitud
    BEGIN
        SELECT @apoyo = CONCAT('SUM(ISNULL(', COLUMN_NAME, ', 0))+')
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'nombre'
        AND ORDINAL_POSITION = @contador

        SET @sql = CONCAT(@sql, @apoyo)
        SET @contador = @contador + 1
    END

    SET @sql = LEFT(@sql, LEN(@sql)-1)
    SET @sql = CONCAT('SELECT @resultadoSUM=', @sql, ' FROM nombre')
    DECLARE @parametros nvarchar(100) = N'@resultadoSUM int OUTPUT'
    EXECUTE sp_executesql @sql, @parametros, @resultadoSUM = @resultado OUTPUT

    RETURN @resultado
END


DECLARE @nombre1 varchar(20) = 'MARTHA'
DECLARE @nombre2 varchar(20) = 'MARTA'
DECLARE @resultado int

EXEC @resultado = dbo.CalcularSuma @nombre1, @nombre2;

PRINT @resultado
