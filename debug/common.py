import os,shutil
from pathlib import Path

def delete_file(file_to_delete):
    try:
        shutil.rmtree(file_to_delete)
        print(f"INFO: {file_to_delete} has been deleted.")
    except Exception as e:
        try:
            os.remove(file_to_delete)
            print(f"{file_to_delete} has been deleted.")
        except Exception as e:
            pass

def move_file(source_path,destination_directory):
    print("INFO: Moving file from", source_path, "to", destination_directory)
    try:
        source_path=Path(source_path)
        destination_directory=Path(destination_directory)
        source_path.rename(destination_directory)
        return True
    except Exception as e:
        return False

def write_file(text,file_name):
    fo=open(file_name,"w")
    for x in text.split('\n'):
        fo.write(x)
        fo.write("\n")
    fo.close()