import subprocess
import os
import datetime

SCRIPT_PATH = os.path.abspath(__file__) 
BACKEND_PATH = os.path.dirname(SCRIPT_PATH) 
PROJECT_ROOT = os.path.dirname(BACKEND_PATH) 
REACT_PATH = os.path.join(PROJECT_ROOT, "ipo_tracker") 
BACKEND_JSON = os.path.join(BACKEND_PATH, "ipo_dashboard.json") 
REACT_JSON = os.path.join(REACT_PATH, "public", "ipo_react.json")

# def get_file_paths(): #function to return the path of files making it dynamic removing the function because its not really needed
#     script_path=os.path.abspath(__file__)
#     backend_path=os.path.dirname(script_path)
#     main_directory_path=os.path.dirname(backend_path)
#     react_path=os.path.join(main_directory_path,"ipo_tracker")
#     backend_json_file=os.path.join(backend_path,"ipo_dashboard.json")
#     react_json_file = os.path.join(react_path, "public", "ipo_react.json") 
#     return backend_path, main_directory_path, react_path, backend_json_file,react_json_file


def run_scraper():
    print("Running scraper...")
    subprocess.run(["python", os.path.join(BACKEND_PATH,"web_scraper.py"),BACKEND_JSON], check=True)

def run_cpp():
    print("Compiling C++ program...")
  
    subprocess.run(["g++",os.path.join(BACKEND_PATH,"logic.cpp") , "-o", os.path.join(BACKEND_PATH,"logic")], check=True)
    print("Running C++ processor...")
    exe = os.path.join(BACKEND_PATH,"logic.exe") if os.name == "nt" else os.path.join(BACKEND_PATH,".logic")
    subprocess.run([exe,BACKEND_JSON,REACT_JSON], check=True)

def run_react():
    print("Starting react app")
    
    
    os.chdir(REACT_PATH) #changing directory to correct directory to run the react app
    subprocess.run("npm run dev",shell=True,check=True)

def should_update():
    

    # If the data processors have never run before we need to run them regardless of the time
    if not os.path.exists(BACKEND_JSON):
        return True

    # Rule 2: If JSON is older than 6 hours → force update
    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(BACKEND_JSON))
    now = datetime.datetime.now()
    age_hours = (now - last_modified).total_seconds() / 3600
    if age_hours >= 6:
        return True

    # Rule 3: Scheduled times (10 AM and 8 PM)
    if (now.hour == 10 or now.hour == 20) and now.minute < 10:
        return True

    # Otherwise → skip backend
    return False
def run():
    if should_update():
        run_scraper()
        run_cpp()

    run_react()    
def main():
    run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nReact app stopped by user. Exiting orchestrator...")

