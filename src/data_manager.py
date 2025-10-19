"""
Data Manager for Persistent Storage
==================================

Handles saving and loading of uploaded datasets across page refreshes.
"""

import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import pickle

class DataManager:
    """Manages persistent storage of uploaded datasets"""
    
    def __init__(self, data_dir="data/uploaded"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.data_dir / "metadata.json"
        self._load_metadata()
    
    def _load_metadata(self):
        """Load metadata from file"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
            except:
                self.metadata = {}
        else:
            self.metadata = {}
    
    def _save_metadata(self):
        """Save metadata to file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def save_dataset(self, df, name, description="", source="uploaded"):
        """Save a dataset with metadata"""
        # Generate unique ID
        dataset_id = f"{int(datetime.now().timestamp())}_{name.replace(' ', '_')}"
        
        # Save the dataframe
        data_file = self.data_dir / f"{dataset_id}.pkl"
        df.to_pickle(data_file)
        
        # Save metadata
        self.metadata[dataset_id] = {
            "name": name,
            "description": description,
            "source": source,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "created_at": datetime.now().isoformat(),
            "file_path": str(data_file)
        }
        
        self._save_metadata()
        return dataset_id
    
    def load_dataset(self, dataset_id):
        """Load a dataset by ID"""
        if dataset_id not in self.metadata:
            return None, "Dataset not found"
        
        try:
            file_path = self.metadata[dataset_id]["file_path"]
            df = pd.read_pickle(file_path)
            return df, None
        except Exception as e:
            return None, f"Error loading dataset: {e}"
    
    def list_datasets(self):
        """List all available datasets"""
        return self.metadata
    
    def delete_dataset(self, dataset_id):
        """Delete a dataset"""
        if dataset_id not in self.metadata:
            return False, "Dataset not found"
        
        try:
            # Delete the data file
            file_path = self.metadata[dataset_id]["file_path"]
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Remove from metadata
            del self.metadata[dataset_id]
            self._save_metadata()
            return True, None
        except Exception as e:
            return False, f"Error deleting dataset: {e}"
    
    def get_dataset_info(self, dataset_id):
        """Get information about a dataset"""
        return self.metadata.get(dataset_id, None)
    
    def clear_all(self):
        """Clear all datasets (use with caution)"""
        try:
            # Delete all data files
            for dataset_id, info in self.metadata.items():
                file_path = info["file_path"]
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            # Clear metadata
            self.metadata = {}
            self._save_metadata()
            return True, None
        except Exception as e:
            return False, f"Error clearing datasets: {e}"

# Global instance
data_manager = DataManager()
