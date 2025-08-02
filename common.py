import os, shutil
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
            print(f"ERROR: {file_to_delete} could not be deleted. Error: {e}")

def move_file(source_path, destination_path):
    print("INFO: Moving file from", source_path, "to", destination_path)
    try:
        source_path = Path(source_path)
        destination_path = Path(destination_path)

        # Ensure destination directory exists
        destination_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(str(source_path), str(destination_path))
        return True
    except Exception as e:
        print("ERROR:", e)
        return False

def write_file(text, file_name):
    fo=open(file_name,"w")
    for x in text.split('\n'):
        fo.write(x)
        fo.write("\n")
    fo.close()