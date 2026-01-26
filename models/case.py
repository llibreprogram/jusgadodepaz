class Case:
    def __init__(self, numero_carpeta, categoria, etapa_procesal, victima, investigado,
                 fecha_denuncia, fecha_formalizacion, fecha_acusacion, fecha_sentencia,
                 fecha_archivo, estado_actual, resultado, apelacion,
                 fiscal_asignado, tiene_citacion=0, fecha_emision_citacion=None, 
                 fecha_comparecencia=None, estado_citacion=None, observaciones_citacion=None,
                 tiene_orden_arresto=0, fecha_emision_orden=None, estado_orden=None,
                 fecha_cumplimiento_orden=None, observaciones_orden=None, origen_orden_arresto=None,
                 fiscal_inicial=None, departamento_actual=None, fiscal_cierre=None,
                 monto_pension=None,
                 cedula_victima=None, cedula_investigado=None,
                 id=None, created_at=None, updated_at=None):
        self.id = id
        self.numero_carpeta = numero_carpeta
        self.categoria = categoria
        self.etapa_procesal = etapa_procesal
        self.victima = victima
        self.investigado = investigado
        self.fecha_denuncia = fecha_denuncia
        self.fecha_formalizacion = fecha_formalizacion
        self.fecha_acusacion = fecha_acusacion
        self.fecha_sentencia = fecha_sentencia
        self.fecha_archivo = fecha_archivo
        self.estado_actual = estado_actual
        self.resultado = resultado
        self.apelacion = apelacion
        self.fiscal_asignado = fiscal_asignado
        self.tiene_citacion = tiene_citacion
        self.fecha_emision_citacion = fecha_emision_citacion
        self.fecha_comparecencia = fecha_comparecencia
        self.estado_citacion = estado_citacion
        self.observaciones_citacion = observaciones_citacion
        self.tiene_orden_arresto = tiene_orden_arresto
        self.fecha_emision_orden = fecha_emision_orden
        self.estado_orden = estado_orden
        self.fecha_cumplimiento_orden = fecha_cumplimiento_orden
        self.observaciones_orden = observaciones_orden
        self.origen_orden_arresto = origen_orden_arresto
        self.fiscal_inicial = fiscal_inicial
        self.departamento_actual = departamento_actual
        self.fiscal_cierre = fiscal_cierre
        self.monto_pension = monto_pension
        self.cedula_victima = cedula_victima
        self.cedula_investigado = cedula_investigado
        self.created_at = created_at
        self.updated_at = updated_at

    def to_tuple(self):
        return (
            self.numero_carpeta,
            self.categoria,
            self.etapa_procesal,
            self.victima,
            self.investigado,
            self.fecha_denuncia,
            self.fecha_formalizacion,
            self.fecha_acusacion,
            self.fecha_sentencia,
            self.fecha_archivo,
            self.estado_actual,
            self.resultado,
            self.apelacion,
            self.fiscal_asignado,
            self.tiene_citacion,
            self.fecha_emision_citacion,
            self.fecha_comparecencia,
            self.estado_citacion,
            self.observaciones_citacion,
            self.tiene_orden_arresto,
            self.fecha_emision_orden,
            self.estado_orden,
            self.fecha_cumplimiento_orden,
            self.observaciones_orden,
            self.origen_orden_arresto,
            self.fiscal_inicial,
            self.departamento_actual,
            self.fiscal_cierre,
            self.monto_pension,
            self.cedula_victima,
            self.cedula_investigado,
        )

    @staticmethod
    def from_row(row):
        # Handle both old schema and new schema with citations and fiscal tracking
        if len(row) >= 34:  # New schema with cedulas (31 fields + id + created/updated)
            return Case(
                numero_carpeta=row[1],
                categoria=row[2],
                etapa_procesal=row[3],
                victima=row[4],
                investigado=row[5],
                fecha_denuncia=row[6],
                fecha_formalizacion=row[7],
                fecha_acusacion=row[8],
                fecha_sentencia=row[9],
                fecha_archivo=row[10],
                estado_actual=row[11],
                resultado=row[12],
                apelacion=row[13],
                fiscal_asignado=row[14],
                tiene_citacion=row[15] if len(row) > 15 else 0,
                fecha_emision_citacion=row[16] if len(row) > 16 else None,
                fecha_comparecencia=row[17] if len(row) > 17 else None,
                estado_citacion=row[18] if len(row) > 18 else None,
                observaciones_citacion=row[19] if len(row) > 19 else None,
                tiene_orden_arresto=row[20] if len(row) > 20 else 0,
                fecha_emision_orden=row[21] if len(row) > 21 else None,
                estado_orden=row[22] if len(row) > 22 else None,
                fecha_cumplimiento_orden=row[23] if len(row) > 23 else None,
                observaciones_orden=row[24] if len(row) > 24 else None,
                origen_orden_arresto=row[25] if len(row) > 25 else None,
                fiscal_inicial=row[26] if len(row) > 26 else None,
                departamento_actual=row[27] if len(row) > 27 else None,
                fiscal_cierre=row[28] if len(row) > 28 else None,
                monto_pension=row[29] if len(row) > 29 else None,
                cedula_victima=row[30] if len(row) > 30 else None,
                cedula_investigado=row[31] if len(row) > 31 else None,
                id=row[0],
                created_at=row[32] if len(row) > 32 else None,
                updated_at=row[33] if len(row) > 33 else None
            )
        elif len(row) >= 32:  # Schema with monto_pension (29 fields + id + created/updated)
            return Case(
                numero_carpeta=row[1],
                categoria=row[2],
                etapa_procesal=row[3],
                victima=row[4],
                investigado=row[5],
                fecha_denuncia=row[6],
                fecha_formalizacion=row[7],
                fecha_acusacion=row[8],
                fecha_sentencia=row[9],
                fecha_archivo=row[10],
                estado_actual=row[11],
                resultado=row[12],
                apelacion=row[13],
                fiscal_asignado=row[14],
                tiene_citacion=row[15] if len(row) > 15 else 0,
                fecha_emision_citacion=row[16] if len(row) > 16 else None,
                fecha_comparecencia=row[17] if len(row) > 17 else None,
                estado_citacion=row[18] if len(row) > 18 else None,
                observaciones_citacion=row[19] if len(row) > 19 else None,
                tiene_orden_arresto=row[20] if len(row) > 20 else 0,
                fecha_emision_orden=row[21] if len(row) > 21 else None,
                estado_orden=row[22] if len(row) > 22 else None,
                fecha_cumplimiento_orden=row[23] if len(row) > 23 else None,
                observaciones_orden=row[24] if len(row) > 24 else None,
                origen_orden_arresto=row[25] if len(row) > 25 else None,
                fiscal_inicial=row[26] if len(row) > 26 else None,
                departamento_actual=row[27] if len(row) > 27 else None,
                fiscal_cierre=row[28] if len(row) > 28 else None,
                id=row[0],
                created_at=row[29] if len(row) > 29 else None,
                updated_at=row[30] if len(row) > 30 else None
            )
        elif len(row) >= 27:  # Schema with citations but without fiscal fields
            return Case(
                numero_carpeta=row[1],
                categoria=row[2],
                etapa_procesal=row[3],
                victima=row[4],
                investigado=row[5],
                fecha_denuncia=row[6],
                fecha_formalizacion=row[7],
                fecha_acusacion=row[8],
                fecha_sentencia=row[9],
                fecha_archivo=row[10],
                estado_actual=row[11],
                resultado=row[12],
                apelacion=row[13],
                fiscal_asignado=row[14],
                tiene_citacion=row[15] if len(row) > 15 else 0,
                fecha_emision_citacion=row[16] if len(row) > 16 else None,
                fecha_comparecencia=row[17] if len(row) > 17 else None,
                estado_citacion=row[18] if len(row) > 18 else None,
                observaciones_citacion=row[19] if len(row) > 19 else None,
                tiene_orden_arresto=row[20] if len(row) > 20 else 0,
                fecha_emision_orden=row[21] if len(row) > 21 else None,
                estado_orden=row[22] if len(row) > 22 else None,
                fecha_cumplimiento_orden=row[23] if len(row) > 23 else None,
                observaciones_orden=row[24] if len(row) > 24 else None,
                origen_orden_arresto=row[25] if len(row) > 25 else None,
                id=row[0],
                created_at=row[26] if len(row) > 26 else None,
                updated_at=row[27] if len(row) > 27 else None
            )
        elif len(row) >= 17:
            # Old schema with created_at, updated_at
            return Case(
                numero_carpeta=row[1],
                categoria=row[2],
                etapa_procesal=row[3],
                victima=row[4],
                investigado=row[5],
                fecha_denuncia=row[6],
                fecha_formalizacion=row[7],
                fecha_acusacion=row[8],
                fecha_sentencia=row[9],
                fecha_archivo=row[10],
                estado_actual=row[11],
                resultado=row[12],
                apelacion=row[13],
                fiscal_asignado=row[14],
                id=row[0],
                created_at=row[15],
                updated_at=row[16]
            )
        else:
            # Old schema
            return Case(*row[1:], id=row[0])