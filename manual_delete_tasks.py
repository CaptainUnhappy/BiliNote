
import sqlite3
import os
import json

# Define paths
DB_PATH = os.path.join("docker_data", "data", "bili_note.db")
NOTES_DIR = os.path.join("docker_data", "notes")

def get_task_title(task_id):
    """Try to get title from result or status json file."""
    # Try result file first
    result_path = os.path.join(NOTES_DIR, f"{task_id}.json")
    if os.path.exists(result_path):
        try:
            with open(result_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('audio_meta', {}).get('title', 'Unknown Title')
        except:
            pass
            
    # Try status file
    status_path = os.path.join(NOTES_DIR, f"{task_id}.status.json")
    if os.path.exists(status_path):
        try:
            with open(status_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('audio_meta', {}).get('title', 'Unknown Title (Status File)')
        except:
            pass
            
    return "Unknown Title"

def list_and_delete_tasks():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at: {DB_PATH}")
        print("Please ensure you are running this script from the project root directory (where docker-compose.yml is).")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Select all tasks
        cursor.execute("SELECT id, video_id, task_id, platform, created_at FROM video_tasks ORDER BY created_at DESC")
        tasks = cursor.fetchall()
        
        if not tasks:
            print("No tasks found in database.")
            conn.close()
            return

        print(f"\nFound {len(tasks)} tasks:")
        print("-" * 120)
        print(f"{'Idx':<5} | {'Platform':<10} | {'Created At':<20} | {'Video ID':<20} | {'Title'}")
        print("-" * 120)

        task_map = {}
        for idx, task in enumerate(tasks):
            db_id, video_id, task_id, platform, created_at = task
            title = get_task_title(task_id)
            print(f"{idx+1:<5} | {platform:<10} | {created_at:<20} | {video_id:<20} | {title}")
            task_map[idx+1] = (video_id, platform, task_id)

        print("-" * 120)
        print("\nEnter task numbers to delete (e.g., '1 3 5'), or 'all' to delete all, or 'q' to quit.")
        choice = input("Selection: ").strip()

        if choice.lower() == 'q':
            print("Exiting.")
            conn.close()
            return
            
        ids_to_delete = [] # List of (video_id, platform, task_id)
        
        if choice.lower() == 'all':
             ids_to_delete = list(task_map.values())
        else:
            try:
                selected_indices = [int(x) for x in choice.split()]
                for idx in selected_indices:
                    if idx in task_map:
                        ids_to_delete.append(task_map[idx])
                    else:
                        print(f"Warning: Invalid index {idx} ignored.")
            except ValueError:
                print("Invalid input. Please enter numbers.")
                conn.close()
                return

        if not ids_to_delete:
            print("No tasks selected.")
            conn.close()
            return

        print(f"\nDeleting {len(ids_to_delete)} tasks...")
        
        deleted_count = 0
        for video_id, platform, task_id in ids_to_delete:
            # Delete from DB
            cursor.execute("DELETE FROM video_tasks WHERE video_id = ? AND platform = ?", (video_id, platform))
            if cursor.rowcount > 0:
                deleted_count += 1
                
                # Optional: Delete files?
                try:
                    result_file = os.path.join(NOTES_DIR, f"{task_id}.json")
                    status_file = os.path.join(NOTES_DIR, f"{task_id}.status.json")
                    if os.path.exists(result_file): os.remove(result_file)
                    if os.path.exists(status_file): os.remove(status_file)
                except Exception as ex:
                    print(f"  Warning: Failed to delete files for {task_id}: {ex}")
            
        conn.commit()
        print(f"Successfully deleted {deleted_count} tasks from database and cleaned up associated files.")
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_and_delete_tasks()
