import sys
import shutil
import subprocess
from pathlib import Path
import sys
from config.config_loader import BASE_PATH, CONFIG_PATH, script_version, INTERNAL_NAME
from util.logger import console
from util.lang import lang
from util.util import pause, sleep

def send_to_friend():
    # Create _toCompress directory
    to_compress_dir = BASE_PATH / "_toCompress"
    to_compress_dir.mkdir(exist_ok=True)
    
    # Copy this.exe and _GVU to _toCompress
    script_path = Path(sys.executable)
    gvu_path = BASE_PATH / INTERNAL_NAME
    
    shutil.copy2(script_path, to_compress_dir / script_path.name)
    console.print(lang["send_to_friend.copied_exe"](exe_name=script_path.name))
    
    if gvu_path.exists():
        gvu_copy = to_compress_dir / INTERNAL_NAME
        if gvu_copy.exists():
            shutil.rmtree(gvu_copy)
        shutil.copytree(gvu_path, gvu_copy)
        console.print(lang["send_to_friend.copied_internals"](_internals=INTERNAL_NAME))
    else:
        raise FileNotFoundError(gvu_path)
    
    # Delete gvu_config.ini
    config_to_delete = to_compress_dir / CONFIG_PATH.relative_to(BASE_PATH)
    if config_to_delete.exists():
        config_to_delete.unlink()
        console.print(lang["send_to_friend.deleted_config"](config_path=config_to_delete))
        console.print()
    
    # Compress _toCompress to versioned ZIP
    exe_name = script_path.stem
    zip_name = f"{exe_name}_{script_version}"
    zip_path = BASE_PATH / zip_name
    
    shutil.make_archive(str(zip_path), 'zip', to_compress_dir)
    console.print(lang["send_to_friend.created_zip"](zip_name=zip_name))
    
    shutil.rmtree(to_compress_dir)

    console.print(lang["send_to_friend.send_guide"])
    pause()
    console.print(lang["send_to_friend.opening_folder"](folder_path=BASE_PATH))
    sleep(1)

    # Open folder destination
    subprocess.Popen(f'explorer /select,"{zip_path}.zip"')