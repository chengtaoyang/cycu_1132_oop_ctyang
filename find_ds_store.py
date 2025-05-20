import os

def find_ds_store_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == '.DS_Store':
                print(os.path.join(dirpath, filename))

if __name__ == "__main__":
    find_ds_store_files(".")
