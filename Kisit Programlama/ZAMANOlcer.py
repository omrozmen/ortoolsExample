import os
import time
import csv
import subprocess



def measure_execution_time(file_name, timeout=10):
    """Measure the execution time of a Python script with a timeout."""
    start_time = time.time()
    try:
        subprocess.run(['python3', file_name], capture_output=True, check=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"Timeout expired for {file_name}")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error executing {file_name}: {e}")
        return None
    end_time = time.time()
    return end_time - start_time

def measure_all_files(directory):
    # List all files in the given directory
    files = os.listdir(directory)
    
    # Filter out only .py files
    py_files = [file for file in files if file.endswith('.py')]
    
    print(f"Found {len(py_files)} Python files in the directory '{directory}'.")
    
    # Measure and store the execution time for each .py file
    execution_times = []
    for py_file in py_files:
        file_path = os.path.join(directory, py_file)
        print(f"Measuring execution time for {file_path}...")
        execution_time = measure_execution_time(file_path)
        if execution_time is not None:
            execution_times.append((py_file, execution_time))
            print(f"Execution time for {py_file}: {execution_time:.4f} seconds")
        else:
            execution_times.append((py_file, "Timeout or Error"))
    
    # Sort the execution times in descending order
    execution_times.sort(key=lambda x: x[1] if isinstance(x[1], (int, float)) else float('inf'), reverse=True)
    
    # Save execution times to a CSV file
    csv_file_path = os.path.join(directory, 'execution_times.csv')
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File Name', 'Execution Time (seconds)'])
        writer.writerows(execution_times)
    
    print(f"Execution times have been saved to '{csv_file_path}'.")

if __name__ == "__main__":
    # Example usage: measure all files in a specific directory
    directory_to_measure = 'Zamanolcumu/'  # Burada dosya yolunu belirtin
    # directory_to_measure = 'C:\\Users\\your_username\\my_python_scripts'  # Windows için
    measure_all_files(directory_to_measure)
