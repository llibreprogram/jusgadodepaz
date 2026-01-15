import sqlite3
from datetime import datetime
from contextlib import contextmanager
import threading

class Database:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, db_path='cases.db'):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, db_path='cases.db'):
        if not hasattr(self, 'initialized'):
            self.db_path = db_path
            self.local = threading.local()
            self.create_table()
            self.create_indexes()
            self.initialized = True
    
    def get_connection(self):
        """Get thread-local connection"""
        if not hasattr(self.local, 'conn') or self.local.conn is None:
            self.local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.local.conn.row_factory = sqlite3.Row
        return self.local.conn
    
    @contextmanager
    def transaction(self):
        """Context manager for transactions with automatic rollback on error"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
    
    def create_indexes(self):
        """Create database indexes for better query performance"""
        conn = self.get_connection()
        cursor = conn.cursor()
        indexes = [
            'CREATE INDEX IF NOT EXISTS idx_numero_carpeta ON cases(numero_carpeta)',
            'CREATE INDEX IF NOT EXISTS idx_fecha_denuncia ON cases(fecha_denuncia)',
            'CREATE INDEX IF NOT EXISTS idx_fiscal ON cases(fiscal_asignado)',
            'CREATE INDEX IF NOT EXISTS idx_estado ON cases(estado_actual)',
            'CREATE INDEX IF NOT EXISTS idx_categoria ON cases(categoria)',
        ]
        for index_sql in indexes:
            cursor.execute(index_sql)
        conn.commit()

    def create_table(self):
        with self.transaction() as cursor:
            cursor.execute("PRAGMA table_info(cases)")
            cols = [row[1] for row in cursor.fetchall()]
            
            # Check if table exists and has old schema
            if cols and 'created_at' not in cols:
                # SQLite ALTER TABLE limitation: can't use CURRENT_TIMESTAMP in ALTER
                # Add columns with NULL default, then update existing rows
                cursor.execute("ALTER TABLE cases ADD COLUMN created_at TIMESTAMP")
                cursor.execute("ALTER TABLE cases ADD COLUMN updated_at TIMESTAMP")
                cursor.execute("UPDATE cases SET created_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
            
            # Add arrest warrant columns if they don't exist
            if cols and 'tiene_orden_arresto' not in cols:
                cursor.execute("ALTER TABLE cases ADD COLUMN tiene_orden_arresto INTEGER DEFAULT 0")
                cursor.execute("ALTER TABLE cases ADD COLUMN fecha_emision_orden TEXT")
                cursor.execute("ALTER TABLE cases ADD COLUMN estado_orden TEXT")
                cursor.execute("ALTER TABLE cases ADD COLUMN fecha_cumplimiento_orden TEXT")
                cursor.execute("ALTER TABLE cases ADD COLUMN observaciones_orden TEXT")
            
            # Add citation columns if they don't exist
            if cols and 'tiene_citacion' not in cols:
                cursor.execute("ALTER TABLE cases ADD COLUMN tiene_citacion INTEGER DEFAULT 0")
                cursor.execute("ALTER TABLE cases ADD COLUMN fecha_emision_citacion TEXT")
                cursor.execute("ALTER TABLE cases ADD COLUMN fecha_comparecencia TEXT")
                cursor.execute("ALTER TABLE cases ADD COLUMN estado_citacion TEXT")
                cursor.execute("ALTER TABLE cases ADD COLUMN observaciones_citacion TEXT")
            
            # Add origin column to arrest warrant if it doesn't exist
            if cols and 'origen_orden_arresto' not in cols:
                cursor.execute("ALTER TABLE cases ADD COLUMN origen_orden_arresto TEXT")
            
            # Add fiscal tracking columns if they don't exist
            if cols and 'fiscal_inicial' not in cols:
                cursor.execute("ALTER TABLE cases ADD COLUMN fiscal_inicial TEXT")
                cursor.execute("ALTER TABLE cases ADD COLUMN departamento_actual TEXT")
                cursor.execute("ALTER TABLE cases ADD COLUMN fiscal_cierre TEXT")
                # Migrate existing data: fiscal_asignado becomes fiscal_inicial and fiscal_actual
                cursor.execute("UPDATE cases SET fiscal_inicial = fiscal_asignado WHERE fiscal_inicial IS NULL")
            
            # Add monto_pension column if it doesn't exist
            if cols and 'monto_pension' not in cols:
                cursor.execute("ALTER TABLE cases ADD COLUMN monto_pension REAL")
            
            if not cols:
                # Table doesn't exist, create with full schema
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cases (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        numero_carpeta TEXT UNIQUE NOT NULL,
                        categoria TEXT,
                        etapa_procesal TEXT,
                        victima TEXT,
                        investigado TEXT,
                        fecha_denuncia TEXT,
                        fecha_formalizacion TEXT,
                        fecha_acusacion TEXT,
                        fecha_sentencia TEXT,
                        fecha_archivo TEXT,
                        estado_actual TEXT,
                        resultado TEXT,
                        apelacion INTEGER,
                        fiscal_asignado TEXT,
                        tiene_citacion INTEGER DEFAULT 0,
                        fecha_emision_citacion TEXT,
                        fecha_comparecencia TEXT,
                        estado_citacion TEXT,
                        observaciones_citacion TEXT,
                        tiene_orden_arresto INTEGER DEFAULT 0,
                        fecha_emision_orden TEXT,
                        estado_orden TEXT,
                        fecha_cumplimiento_orden TEXT,
                        observaciones_orden TEXT,
                        origen_orden_arresto TEXT,
                        fiscal_inicial TEXT,
                        departamento_actual TEXT,
                        fiscal_cierre TEXT,
                        monto_pension REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            
            # Create fiscal history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historial_fiscales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    caso_id INTEGER NOT NULL,
                    fiscal_nombre TEXT NOT NULL,
                    departamento TEXT,
                    accion TEXT NOT NULL,
                    fiscal_destino TEXT,
                    departamento_destino TEXT,
                    motivo TEXT,
                    fecha_movimiento TEXT NOT NULL,
                    observaciones TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (caso_id) REFERENCES cases(id) ON DELETE CASCADE
                )
            ''')

    def insert_case(self, case_data):
        with self.transaction() as cursor:
            cursor.execute('''
                INSERT INTO cases (
                    numero_carpeta, categoria, etapa_procesal, victima, investigado,
                    fecha_denuncia, fecha_formalizacion, fecha_acusacion, fecha_sentencia,
                    fecha_archivo, estado_actual, resultado, apelacion,
                    fiscal_asignado, tiene_citacion, fecha_emision_citacion, fecha_comparecencia,
                    estado_citacion, observaciones_citacion, tiene_orden_arresto, fecha_emision_orden, 
                    estado_orden, fecha_cumplimiento_orden, observaciones_orden, origen_orden_arresto,
                    fiscal_inicial, departamento_actual, fiscal_cierre, monto_pension,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''', case_data)
            return cursor.lastrowid

    def update_case(self, case_id, case_data):
        with self.transaction() as cursor:
            cursor.execute('''
                UPDATE cases SET
                    numero_carpeta = ?,
                    categoria = ?,
                    etapa_procesal = ?,
                    victima = ?,
                    investigado = ?,
                    fecha_denuncia = ?,
                    fecha_formalizacion = ?,
                    fecha_acusacion = ?,
                    fecha_sentencia = ?,
                    fecha_archivo = ?,
                    estado_actual = ?,
                    resultado = ?,
                    apelacion = ?,
                    fiscal_asignado = ?,
                    tiene_citacion = ?,
                    fecha_emision_citacion = ?,
                    fecha_comparecencia = ?,
                    estado_citacion = ?,
                    observaciones_citacion = ?,
                    tiene_orden_arresto = ?,
                    fecha_emision_orden = ?,
                    estado_orden = ?,
                    fecha_cumplimiento_orden = ?,
                    observaciones_orden = ?,
                    origen_orden_arresto = ?,
                    fiscal_inicial = ?,
                    departamento_actual = ?,
                    fiscal_cierre = ?,
                    monto_pension = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (*case_data, case_id))

    def delete_case(self, case_id):
        with self.transaction() as cursor:
            cursor.execute('DELETE FROM cases WHERE id = ?', (case_id,))

    def get_case_by_carpeta(self, numero_carpeta):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cases WHERE numero_carpeta = ?', (numero_carpeta,))
        return cursor.fetchone()

    def get_all_cases(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        # Try to order by updated_at if it exists, fallback to id
        try:
            cursor.execute('SELECT * FROM cases ORDER BY updated_at DESC')
        except sqlite3.OperationalError:
            cursor.execute('SELECT * FROM cases ORDER BY id DESC')
        return cursor.fetchall()
    
    def close_connection(self):
        """Close thread-local connection"""
        if hasattr(self.local, 'conn') and self.local.conn is not None:
            self.local.conn.close()
            self.local.conn = None
    
    # Fiscal History Methods
    def insert_fiscal_history(self, history_data):
        """Insert a new fiscal history entry"""
        with self.transaction() as cursor:
            cursor.execute('''
                INSERT INTO historial_fiscales (
                    caso_id, fiscal_nombre, departamento, accion,
                    fiscal_destino, departamento_destino, motivo,
                    fecha_movimiento, observaciones
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', history_data)
            return cursor.lastrowid
    
    def get_fiscal_history(self, caso_id):
        """Get all fiscal history for a case, ordered by date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM historial_fiscales 
            WHERE caso_id = ? 
            ORDER BY fecha_movimiento ASC, created_at ASC
        ''', (caso_id,))
        return cursor.fetchall()
    
    def delete_fiscal_history(self, history_id):
        """Delete a specific fiscal history entry"""
        with self.transaction() as cursor:
            cursor.execute('DELETE FROM historial_fiscales WHERE id = ?', (history_id,))
    
    def get_fiscal_statistics(self):
        """Get statistics about fiscal assignments and transfers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Cases received by each fiscal (inicial)
        cursor.execute('''
            SELECT fiscal_inicial, COUNT(*) as count 
            FROM cases 
            WHERE fiscal_inicial IS NOT NULL AND fiscal_inicial != ''
            GROUP BY fiscal_inicial
        ''')
        stats['recibidos'] = dict(cursor.fetchall())
        
        # Cases currently assigned
        cursor.execute('''
            SELECT fiscal_asignado, COUNT(*) as count 
            FROM cases 
            WHERE fiscal_asignado IS NOT NULL AND fiscal_asignado != ''
            GROUP BY fiscal_asignado
        ''')
        stats['asignados'] = dict(cursor.fetchall())
        
        # Cases closed by each fiscal
        cursor.execute('''
            SELECT fiscal_cierre, COUNT(*) as count 
            FROM cases 
            WHERE fiscal_cierre IS NOT NULL AND fiscal_cierre != ''
            GROUP BY fiscal_cierre
        ''')
        stats['cerrados'] = dict(cursor.fetchall())
        
        # Transfer statistics
        cursor.execute('''
            SELECT 
                fiscal_nombre as fiscal_origen,
                COUNT(*) as total_declinaciones
            FROM historial_fiscales 
            WHERE accion IN ('Declinación', 'Transferencia')
            GROUP BY fiscal_nombre
        ''')
        stats['declinaciones_salida'] = dict(cursor.fetchall())
        
        cursor.execute('''
            SELECT 
                fiscal_destino,
                COUNT(*) as total_recepciones
            FROM historial_fiscales 
            WHERE accion IN ('Declinación', 'Transferencia') 
            AND fiscal_destino IS NOT NULL
            GROUP BY fiscal_destino
        ''')
        stats['declinaciones_entrada'] = dict(cursor.fetchall())
        
        return stats
