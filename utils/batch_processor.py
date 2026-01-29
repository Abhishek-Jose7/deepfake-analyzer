"""
Batch Processing Module
Process multiple videos concurrently with progress tracking
"""
import threading
import queue
import time
from datetime import datetime


class BatchProcessor:
    """
    Batch processor for multiple video analyses
    """
    
    def __init__(self, max_workers=3):
        """
        Initialize batch processor
        
        Args:
            max_workers: Maximum concurrent analyses
        """
        self.max_workers = max_workers
        self.jobs = {}
        self.job_queue = queue.Queue()
        self.results = {}
        self.locks = {}
    
    def create_job(self, job_id, files):
        """
        Create a new batch job
        
        Args:
            job_id: Unique job identifier
            files: List of file paths to process
            
        Returns:
            Job configuration
        """
        self.jobs[job_id] = {
            'id': job_id,
            'files': files,
            'total': len(files),
            'completed': 0,
            'status': 'pending',
            'start_time': datetime.now().isoformat(),
            'results': [],
            'errors': []
        }
        self.locks[job_id] = threading.Lock()
        
        return self.jobs[job_id]
    
    def update_job_progress(self, job_id, file_index, result=None, error=None):
        """
        Update job progress
        
        Args:
            job_id: Job identifier
            file_index: Index of completed file
            result: Analysis result (if successful)
            error: Error message (if failed)
        """
        with self.locks[job_id]:
            job = self.jobs[job_id]
            job['completed'] += 1
            
            # Get filename (handle dict format)
            file_info = job['files'][file_index]
            if isinstance(file_info, dict):
                filename = file_info.get('filename', file_info.get('path', 'unknown'))
            else:
                filename = file_info
            
            if result:
                job['results'].append({
                    'file_index': file_index,
                    'filename': filename,
                    'result': result
                })
            
            if error:
                job['errors'].append({
                    'file_index': file_index,
                    'filename': filename,
                    'error': error
                })
            
            # Update status
            if job['completed'] == job['total']:
                job['status'] = 'completed'
                job['end_time'] = datetime.now().isoformat()
            elif job['status'] == 'pending':
                job['status'] = 'processing'
            
            # Calculate progress percentage
            job['progress'] = (job['completed'] / job['total']) * 100
    
    def get_job_status(self, job_id):
        """
        Get current job status
        
        Args:
            job_id: Job identifier
            
        Returns:
            Job status dictionary
        """
        if job_id not in self.jobs:
            return None
        
        with self.locks[job_id]:
            return self.jobs[job_id].copy()
    
    def process_file(self, job_id, file_index, analyze_function):
        """
        Process a single file
        
        Args:
            job_id: Job identifier
            file_index: Index of file to process
            analyze_function: Function to analyze the file
        """
        try:
            file_info = self.jobs[job_id]['files'][file_index]
            # Handle both dict format and string format
            if isinstance(file_info, dict):
                filepath = file_info.get('path', file_info)
            else:
                filepath = file_info
            result = analyze_function(filepath)
            self.update_job_progress(job_id, file_index, result=result)
        except Exception as e:
            self.update_job_progress(job_id, file_index, error=str(e))
    
    def start_batch(self, job_id, analyze_function):
        """
        Start processing a batch job
        
        Args:
            job_id: Job identifier
            analyze_function: Function to analyze each file
        """
        job = self.jobs[job_id]
        threads = []
        
        # Create thread pool
        for i in range(min(self.max_workers, len(job['files']))):
            thread = threading.Thread(
                target=self._worker,
                args=(job_id, analyze_function),
                daemon=True
            )
            thread.start()
            threads.append(thread)
        
        # Add files to queue
        for i in range(len(job['files'])):
            self.job_queue.put((job_id, i))
        
        return threads
    
    def start_processing(self, job_id, analyze_function):
        """
        Alias for start_batch for compatibility
        
        Args:
            job_id: Job identifier
            analyze_function: Function to analyze each file
        """
        return self.start_batch(job_id, analyze_function)
    
    def _worker(self, job_id, analyze_function):
        """
        Worker thread for processing files
        
        Args:
            job_id: Job identifier
            analyze_function: Function to analyze files
        """
        while True:
            try:
                # Get next file from queue (non-blocking with timeout)
                task_job_id, file_index = self.job_queue.get(timeout=1)
                
                # Only process if it's for this job
                if task_job_id == job_id:
                    self.process_file(job_id, file_index, analyze_function)
                    self.job_queue.task_done()
                else:
                    # Put it back if it's for a different job
                    self.job_queue.put((task_job_id, file_index))
                    time.sleep(0.1)
                    
            except queue.Empty:
                # Queue is empty, check if job is done
                with self.locks[job_id]:
                    if self.jobs[job_id]['completed'] == self.jobs[job_id]['total']:
                        break
            except Exception as e:
                print(f"Worker error: {e}")
                break


# Global batch processor instance
batch_processor = BatchProcessor(max_workers=3)
