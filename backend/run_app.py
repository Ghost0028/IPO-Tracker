import subprocess
import os
import datetime

def run_scraper():
    print("Running scraper...")
    subprocess.run(["python", "web_scraper.py"], check=True)

def run_cpp():
    print("Compiling C++ program...")
    subprocess.run(["g++", "logic.cpp", "-o", "logic"], check=True)
    print("Running C++ processor...")
    exe = "logic.exe" if os.name == "nt" else ".logic"
    subprocess.run([exe], check=True)

def run_react():
    print("Starting react app")
    script_path=os.path.abspath(__file__)
    backend_path=os.path.dirname(script_path)
    main_directory_path=os.path.dirname(backend_path)
    react_path=os.path.join(main_directory_path,"ipo_tracker")
    os.chdir(react_path) #changing directory to correct directory to run the react app
    subprocess.run("npm run dev",shell=True,check=True)

def should_update():
    # Path to your JSON file
    json_file = "../ipo_tracker/public/ipo_react.json"

    # If the data processors have never run before we need to run them regardless of the time
    if not os.path.exists(json_file):
        return True

    # Rule 2: If JSON is older than 6 hours → force update
    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(json_file))
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

