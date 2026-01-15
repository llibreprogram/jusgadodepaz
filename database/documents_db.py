# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
from database.db import Database

class DocumentsDatabase:
    """Database handler for case documents"""
    
    def __init__(self):
        self.db = Database()
        self.create_documents_table()
    
    def create_documents_table(self):
        """Create documents table if not exists"""
        with self.db.transaction() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id INTEGER NOT NULL,
                    filename TEXT NOT NULL,
                    original_filename TEXT NOT NULL,
                    filepath TEXT NOT NULL,
                    file_type TEXT,
                    file_size INTEGER,
                    description TEXT,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (case_id) REFERENCES cases(id) ON DELETE CASCADE
                )
            ''')
            
            # Create index for faster lookups
            cursor.execute(
                'CREATE INDEX IF NOT EXISTS idx_documents_case_id ON documents(case_id)'
            )
    
    def add_document(self, case_id, filename, original_filename, filepath, file_type, file_size, description=''):
        """Add a document to the database"""
        with self.db.transaction() as cursor:
            cursor.execute('''
                INSERT INTO documents (case_id, filename, original_filename, filepath, file_type, file_size, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (case_id, filename, original_filename, filepath, file_type, file_size, description))
            return cursor.lastrowid
    
    def get_documents_by_case(self, case_id):
        """Get all documents for a case"""
        conn = self.db.get_connection()
        cursor = conn.execute('''
            SELECT id, case_id, filename, original_filename, filepath, file_type, file_size, description, uploaded_at
            FROM documents
            WHERE case_id = ?
            ORDER BY uploaded_at DESC
        ''', (case_id,))
        return cursor.fetchall()
    
    def get_document_by_id(self, doc_id):
        """Get a specific document"""
        conn = self.db.get_connection()
        cursor = conn.execute('''
            SELECT id, case_id, filename, original_filename, filepath, file_type, file_size, description, uploaded_at
            FROM documents
            WHERE id = ?
        ''', (doc_id,))
        return cursor.fetchone()
    
    def delete_document(self, doc_id):
        """Delete a document from database"""
        with self.db.transaction() as cursor:
            cursor.execute('DELETE FROM documents WHERE id = ?', (doc_id,))
    
    def update_document_description(self, doc_id, description):
        """Update document description"""
        with self.db.transaction() as cursor:
            cursor.execute('''
                UPDATE documents SET description = ? WHERE id = ?
            ''', (description, doc_id))
    
    def get_total_documents_count(self):
        """Get total number of documents"""
        conn = self.db.get_connection()
        cursor = conn.execute('SELECT COUNT(*) FROM documents')
        return cursor.fetchone()[0]
    
    def get_total_documents_size(self):
        """Get total size of all documents in bytes"""
        conn = self.db.get_connection()
        cursor = conn.execute('SELECT SUM(file_size) FROM documents')
        result = cursor.fetchone()[0]
        return result if result else 0
