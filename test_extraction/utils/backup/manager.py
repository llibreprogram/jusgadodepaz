import shutil
import os
from datetime import datetime
from pathlib import Path

class BackupManager:
    def __init__(self, db_path='cases.db', backup_dir='backups'):
        self.db_path = db_path
        self.backup_dir = backup_dir
        self._ensure_backup_dir()
    
    def _ensure_backup_dir(self):
        """Create backup directory if it doesn't exist"""
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, prefix='manual'):
        """Create a backup of the database"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"{prefix}_backup_{timestamp}.db"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        try:
            shutil.copy2(self.db_path, backup_path)
            self._cleanup_old_backups()
            return backup_path
        except Exception as e:
            raise Exception(f"Error al crear respaldo: {str(e)}")
    
    def _cleanup_old_backups(self, keep_count=10):
        """Keep only the most recent backups"""
        backup_files = []
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.db'):
                filepath = os.path.join(self.backup_dir, filename)
                backup_files.append((filepath, os.path.getmtime(filepath)))
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # Delete old backups
        for filepath, _ in backup_files[keep_count:]:
            try:
                os.remove(filepath)
            except Exception:
                pass
    
    def restore_backup(self, backup_path):
        """Restore database from backup"""
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup no encontrado: {backup_path}")
        
        try:
            # Create a safety backup before restore
            safety_backup = f"{self.db_path}.before_restore"
            shutil.copy2(self.db_path, safety_backup)
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            return True
        except Exception as e:
            # Try to restore safety backup if restore failed
            if os.path.exists(safety_backup):
                shutil.copy2(safety_backup, self.db_path)
            raise Exception(f"Error al restaurar respaldo: {str(e)}")
    
    def list_backups(self):
        """List all available backups"""
        backups = []
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.db'):
                filepath = os.path.join(self.backup_dir, filename)
                size = os.path.getsize(filepath)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                backups.append({
                    'filename': filename,
                    'path': filepath,
                    'size': size,
                    'date': mtime
                })
        
        # Sort by date (newest first)
        backups.sort(key=lambda x: x['date'], reverse=True)
        return backups
    
    def auto_backup_on_startup(self):
        """Create automatic backup on application startup"""
        return self.create_backup(prefix='auto')
