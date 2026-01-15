# -*- coding: utf-8 -*-
import os
import shutil
from pathlib import Path
from datetime import datetime
from database.documents_db import DocumentsDatabase

class DocumentService:
    """Service for managing case documents"""
    
    def __init__(self):
        self.docs_db = DocumentsDatabase()
        self.base_path = Path('documents')
        self.base_path.mkdir(exist_ok=True)
        
        # Allowed file extensions
        self.allowed_extensions = {
            '.pdf', '.doc', '.docx', '.txt', '.rtf',  # Documents
            '.jpg', '.jpeg', '.png', '.gif', '.bmp',  # Images
            '.xls', '.xlsx', '.csv',  # Spreadsheets
            '.zip', '.rar', '.7z',  # Archives
            '.mp3', '.mp4', '.avi', '.mov',  # Media
        }
    
    def get_case_folder(self, case_id):
        """Get or create folder for case documents"""
        case_folder = self.base_path / f"case_{case_id}"
        case_folder.mkdir(exist_ok=True)
        return case_folder
    
    def add_document(self, case_id, source_filepath, description=''):
        """Add a document to a case"""
        source_path = Path(source_filepath)
        
        # Validate file exists
        if not source_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {source_filepath}")
        
        # Validate extension
        if source_path.suffix.lower() not in self.allowed_extensions:
            raise ValueError(f"Tipo de archivo no permitido: {source_path.suffix}")
        
        # Get file info
        original_filename = source_path.name
        file_size = source_path.stat().st_size
        file_type = source_path.suffix.lower()
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{original_filename}"
        
        # Get case folder and copy file
        case_folder = self.get_case_folder(case_id)
        dest_path = case_folder / filename
        shutil.copy2(source_filepath, dest_path)
        
        # Add to database
        doc_id = self.docs_db.add_document(
            case_id=case_id,
            filename=filename,
            original_filename=original_filename,
            filepath=str(dest_path),
            file_type=file_type,
            file_size=file_size,
            description=description
        )
        
        return doc_id
    
    def get_documents(self, case_id):
        """Get all documents for a case"""
        return self.docs_db.get_documents_by_case(case_id)
    
    def delete_document(self, doc_id):
        """Delete a document"""
        # Get document info
        doc = self.docs_db.get_document_by_id(doc_id)
        if not doc:
            raise ValueError("Documento no encontrado")
        
        # Delete file
        filepath = Path(doc[4])  # filepath is index 4
        if filepath.exists():
            filepath.unlink()
        
        # Delete from database
        self.docs_db.delete_document(doc_id)
    
    def open_document(self, doc_id):
        """Open a document with default application"""
        doc = self.docs_db.get_document_by_id(doc_id)
        if not doc:
            raise ValueError("Documento no encontrado")
        
        filepath = Path(doc[4])  # filepath is index 4
        if not filepath.exists():
            raise FileNotFoundError("El archivo no existe en el sistema")
        
        # Open with default application
        import subprocess
        import platform
        
        system = platform.system()
        if system == 'Windows':
            os.startfile(filepath)
        elif system == 'Darwin':  # macOS
            subprocess.run(['open', filepath])
        else:  # Linux
            subprocess.run(['xdg-open', filepath])
    
    def update_description(self, doc_id, description):
        """Update document description"""
        self.docs_db.update_document_description(doc_id, description)
    
    def get_storage_info(self):
        """Get storage statistics"""
        total_docs = self.docs_db.get_total_documents_count()
        total_size = self.docs_db.get_total_documents_size()
        
        # Format size
        if total_size < 1024:
            size_str = f"{total_size} B"
        elif total_size < 1024 * 1024:
            size_str = f"{total_size / 1024:.2f} KB"
        elif total_size < 1024 * 1024 * 1024:
            size_str = f"{total_size / (1024 * 1024):.2f} MB"
        else:
            size_str = f"{total_size / (1024 * 1024 * 1024):.2f} GB"
        
        return {
            'total_documents': total_docs,
            'total_size_bytes': total_size,
            'total_size_formatted': size_str
        }
    
    def format_file_size(self, size_bytes):
        """Format file size in human-readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
