  #i will change the folder name from name into id but later on the data base that will be the primary key to etreive the needed info 

final_payload = {
    "student_id" : clean_name,
    "timestamp" : datetime.datetime.now().isoformat(),
    "session_start" : stats
}

server_url = "http://127.0.0.1:8000/report"

print("Attempting to send report to the server....")


try:
    response = requests.post(server_url, json=final_payload, timeout=5)
    if response.status_code == 200:
        print("Sucess! Server received the data ")
    else:
        print(f"Server error: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("Failed: Server is offline. Saving Backup locally...")
    clean_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"backup_report_{clean_time}.json"
    with open(filename,"w") as f:
        json.dump(final_payload, f, indent=4)
        print(f"Data saved succesfully saved to {filename}")
except requests.exceptions.Timeout:
    print("Failed: Server timed out.")
except Exception as e:
    print(f"An error has occured {e}")
