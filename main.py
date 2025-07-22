# from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
# import uvicorn
# import os
# import json
# import asyncio
# from typing import Optional, List, Dict, Any
# import pandas as pd
# from datetime import datetime
# import threading
# import time
# from playwright.async_api import async_playwright
# import shutil
# import uuid
# import tempfile
# import zipfile

# # Initialize FastAPI
# app = FastAPI(title="Multi-Project Automation Hub")

# # Templates
# templates = Jinja2Templates(directory="templates")

# print("Server starting...")
# print("Available imports:")
# print("- FastAPI:", FastAPI.__version__ if hasattr(FastAPI, '__version__') else "imported")
# print("- Playwright: imported")
# print("- Pandas:", pd.__version__)
# print("- All other dependencies: imported")

# class DataManager:
#     """Manages agent and call data using local JSON storage"""
#     def __init__(self, project_name="livevox"):
#         self.project_name = project_name
#         self.local_file = f"{project_name}_data.json"
#         print(f"Using local storage: {self.local_file}")
    
#     def load_data(self):
#         """Load data from local JSON file"""
#         if os.path.exists(self.local_file):
#             try:
#                 with open(self.local_file, 'r') as f:
#                     data = json.load(f)
#                     print(f"Loaded data from {self.local_file}")
#                     return data
#             except Exception as e:
#                 print(f"Error loading {self.local_file}: {e}")
        
#         # Return default structure if file doesn't exist
#         default_data = {"agents": {}, "calls": {}}
#         self.save_data(default_data)
#         return default_data
    
#     def save_data(self, data):
#         """Save data to local JSON file"""
#         try:
#             with open(self.local_file, 'w') as f:
#                 json.dump(data, f, indent=2)
#             print(f"Data saved to {self.local_file}")
#             return True
#         except Exception as e:
#             print(f"Error saving to {self.local_file}: {e}")
#             return False
    
#     def add_agent(self, agent_data):
#         data = self.load_data()
#         agent_id = agent_data['id']
#         data['agents'][agent_id] = agent_data
#         if agent_id not in data['calls']:
#             data['calls'][agent_id] = []
#         self.save_data(data)
    
#     def remove_agent(self, agent_id):
#         data = self.load_data()
#         if agent_id in data['agents']:
#             del data['agents'][agent_id]
#         if agent_id in data['calls']:
#             del data['calls'][agent_id]
#         self.save_data(data)

#     def remove_all_agents(self):
#         data = {"agents": {}, "calls": {}}
#         self.save_data(data)
    
#     def add_call(self, agent_id, call_data):
#         data = self.load_data()
#         if agent_id not in data['calls']:
#             data['calls'][agent_id] = []
#         data['calls'][agent_id].append(call_data)
#         self.save_data(data)
    
#     def remove_all_calls(self, agent_id):
#         data = self.load_data()
#         if agent_id in data['calls']:
#             data['calls'][agent_id] = []
#             self.save_data(data)
    
#     def remove_call(self, agent_id, call_index):
#         data = self.load_data()
#         if agent_id in data['calls'] and 0 <= call_index < len(data['calls'][agent_id]):
#             del data['calls'][agent_id][call_index]
#             self.save_data(data)
    
#     def get_agents(self):
#         return self.load_data()['agents']
    
#     def get_calls(self, agent_id):
#         return self.load_data()['calls'].get(agent_id, [])

# # Global data manager
# data_manager = DataManager()

# @app.get("/", response_class=HTMLResponse)
# async def root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.get("/debug/routes")
# async def debug_routes():
#     """Debug endpoint to see all registered routes"""
#     routes = []
#     for route in app.routes:
#         if hasattr(route, 'methods') and hasattr(route, 'path'):
#             routes.append({
#                 "path": route.path,
#                 "methods": list(route.methods),
#                 "name": getattr(route, 'name', 'unknown')
#             })
#     return {"routes": routes}

# @app.put("/debug/test-put")
# async def test_put(test_data: str = Form(...)):
#     """Simple PUT endpoint to test if PUT requests work"""
#     return {"success": True, "received": test_data}

# @app.post("/debug/test-automation")
# async def test_automation_endpoint(
#     function_type: str = Form(...),
#     agent_id: str = Form(...),
#     start_date: str = Form(...),
#     username: str = Form(...),
#     password: str = Form(...),
#     url: str = Form(...),
#     phone_numbers: Optional[str] = Form(None)
# ):
#     """Test endpoint with same signature as automation endpoint"""
#     print("DEBUG: Test automation endpoint called successfully!")
#     return {
#         "success": True,
#         "message": "Test endpoint works!",
#         "received_data": {
#             "function_type": function_type,
#             "agent_id": agent_id,
#             "start_date": start_date,
#             "username": username,
#             "url": url,
#             "phone_numbers": phone_numbers
#         }
#     }

# @app.get("/debug/endpoints")
# async def list_endpoints():
#     """List all available endpoints"""
#     routes = []
#     for route in app.routes:
#         if hasattr(route, 'methods') and hasattr(route, 'path'):
#             routes.append({
#                 "path": route.path,
#                 "methods": list(route.methods),
#                 "name": getattr(route, 'name', 'unknown')
#             })
#     return {"routes": routes}

# @app.get("/livevox", response_class=HTMLResponse)
# async def livevox_app(request: Request):
#     agents = data_manager.get_agents()
#     return templates.TemplateResponse("livevox.html", {
#         "request": request, 
#         "agents": agents
#     })

# # Agent management endpoints
# @app.post("/api/agents")
# async def create_agent(agent_id: str = Form(...), folder: str = Form(...), locator_id: str = Form(...)):
#     if agent_id in data_manager.get_agents():
#         raise HTTPException(status_code=400, detail="Agent ID already exists")
    
#     agent_data = {
#         'id': agent_id,
#         'folder': folder,
#         'locator_id': locator_id
#     }
#     data_manager.add_agent(agent_data)
#     return {"success": True}

# @app.get("/api/agents")
# async def get_agents():
#     return data_manager.get_agents()

# @app.put("/api/agents/{agent_id}")
# async def update_agent(agent_id: str, agent_id_field: str = Form(..., alias="agent_id"), folder: str = Form(...), locator_id: str = Form(...)):
#     print(f"PUT /api/agents/{agent_id} called with data: agent_id={agent_id_field}, folder={folder}, locator_id={locator_id}")
    
#     try:
#         data = data_manager.load_data()
        
#         if agent_id not in data['agents']:
#             raise HTTPException(status_code=404, detail="Agent not found")
        
#         # The agent_id from the URL is the current ID, agent_id_field is from the form
#         # If agent ID is changing, we need to update the key
#         if agent_id != agent_id_field:
#             if agent_id_field in data['agents']:
#                 raise HTTPException(status_code=400, detail="New Agent ID already exists")
            
#             # Move agent data to new key
#             data['agents'][agent_id_field] = {
#                 'id': agent_id_field,
#                 'folder': folder,
#                 'locator_id': locator_id
#             }
#             del data['agents'][agent_id]
            
#             # Move calls data
#             if agent_id in data['calls']:
#                 data['calls'][agent_id_field] = data['calls'][agent_id]
#                 del data['calls'][agent_id]
#         else:
#             # Just update the existing agent
#             data['agents'][agent_id] = {
#                 'id': agent_id_field,
#                 'folder': folder,
#                 'locator_id': locator_id
#             }
        
#         data_manager.save_data(data)
#         print(f"Agent updated successfully: {agent_id} -> {agent_id_field}")
#         return {"success": True, "new_agent_id": agent_id_field}
        
#     except Exception as e:
#         print(f"Error updating agent: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.delete("/api/agents/{agent_id}")
# async def delete_agent(agent_id: str):
#     data_manager.remove_agent(agent_id)
#     return {"success": True}

# @app.post("/api/agents/{agent_id}/calls")
# async def add_call(agent_id: str, phone: str = Form(...), duration: str = Form(...)):
#     call_data = {'phone': phone, 'duration': duration}
#     data_manager.add_call(agent_id, call_data)
#     return {"success": True}

# @app.get("/api/agents/{agent_id}/calls")
# async def get_calls(agent_id: str):
#     return data_manager.get_calls(agent_id)

# @app.put("/api/agents/{agent_id}/calls/{call_index}")
# async def update_call(agent_id: str, call_index: int, phone: str = Form(...), duration: str = Form(...)):
#     print(f"PUT /api/agents/{agent_id}/calls/{call_index} called with phone={phone}, duration={duration}")
    
#     try:
#         data = data_manager.load_data()
        
#         if agent_id not in data['calls']:
#             raise HTTPException(status_code=404, detail="Agent not found")
        
#         if call_index >= len(data['calls'][agent_id]) or call_index < 0:
#             raise HTTPException(status_code=404, detail="Call not found")
        
#         data['calls'][agent_id][call_index] = {'phone': phone, 'duration': duration}
#         data_manager.save_data(data)
#         print(f"Call updated successfully: agent={agent_id}, index={call_index}")
#         return {"success": True}
        
#     except Exception as e:
#         print(f"Error updating call: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.delete("/api/agents/{agent_id}/calls/{call_index}")
# async def delete_call(agent_id: str, call_index: int):
#     data_manager.remove_call(agent_id, call_index)
#     return {"success": True}

# @app.post("/api/upload-excel")
# async def upload_excel(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
        
#         # Save temp file
#         temp_path = f"temp_{uuid.uuid4().hex}.xlsx"
#         with open(temp_path, "wb") as f:
#             f.write(contents)
        
#         # Read Excel
#         df = pd.read_excel(temp_path, dtype=str)
#         os.remove(temp_path)
        
#         required_cols = {'phone number', 'duration', 'agent ID', 'folder name (name)', 'locator'}
#         if not required_cols.issubset(df.columns):
#             missing = required_cols - set(df.columns)
#             raise HTTPException(status_code=400, detail=f"Missing columns: {', '.join(missing)}")
        
#         agents_created = 0
#         calls_added = 0
        
#         for _, row in df.iterrows():
#             agent_id = str(row.get('agent ID', '')).strip()
#             folder = str(row.get('folder name (name)', '')).strip()
#             locator = str(row.get('locator', '')).strip()
#             phone = str(row.get('phone number', '')).strip()
#             duration = str(row.get('duration', '')).strip()
            
#             if not all([agent_id, folder, locator, phone, duration]):
#                 continue
            
#             # Create agent if doesn't exist
#             if agent_id not in data_manager.get_agents():
#                 agent_data = {
#                     'id': agent_id,
#                     'folder': folder,
#                     'locator_id': locator
#                 }
#                 data_manager.add_agent(agent_data)
#                 agents_created += 1
            
#             # Add call
#             call_data = {'phone': phone, 'duration': duration}
#             data_manager.add_call(agent_id, call_data)
#             calls_added += 1
        
#         return {
#             "success": True,
#             "agents_created": agents_created,
#             "calls_added": calls_added
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/download-template")
# async def download_template():
#     template_data = {
#         'phone number': ['7021234567', '7029876543'],
#         'duration': [65, 123],
#         'agent ID': ['3P_95', '3P_235'],
#         'folder name (name)': ['Chuck', 'Jim'],
#         'locator': ['963665', '976426']
#     }
#     df = pd.DataFrame(template_data)
    
#     filename = "call_upload_template.xlsx"
#     df.to_excel(filename, index=False)
    
#     return FileResponse(
#         filename,
#         filename=filename,
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )

# @app.delete("/api/agents")
# async def delete_all_agents():
#     data_manager.remove_all_agents()
#     return {"success": True}

# @app.delete("/api/agents/{agent_id}/calls")
# async def delete_all_calls_for_agent(agent_id: str):
#     data_manager.remove_all_calls(agent_id)
#     return {"success": True}

# # Store active automation tasks with their temp directories and results
# active_tasks = {}

# # FIXED AUTOMATION ENDPOINT - NO OUTPUT_DIR REQUIRED!
# @app.post("/api/automation/start")
# async def start_automation_fixed(
#     function_type: str = Form(...),
#     agent_id: str = Form(...),
#     start_date: str = Form(...),
#     username: str = Form(...),
#     password: str = Form(...),
#     url: str = Form(...),
#     phone_numbers: Optional[str] = Form(None)
# ):
#     """FIXED: No output_dir required anymore - uses temp directories"""
#     try:
#         print("=" * 50)
#         print("FIXED AUTOMATION ENDPOINT CALLED")
#         print(f"Function parameters received:")
#         print(f"  function_type: {function_type}")
#         print(f"  agent_id: {agent_id}")
#         print(f"  start_date: {start_date}")
#         print(f"  username: {username}")
#         print(f"  url: {url}")
#         print(f"  phone_numbers: {phone_numbers}")
#         print("=" * 50)
        
#         task_id = str(uuid.uuid4())
        
#         # Create temporary directory for this task
#         temp_dir = tempfile.mkdtemp(prefix=f"livevox_{task_id}_")
#         print(f"Created temp directory: {temp_dir}")
        
#         config = {
#             'function_type': function_type,
#             'agent_id': agent_id,
#             'start_date': start_date,
#             'temp_dir': temp_dir,
#             'username': username,
#             'password': password,
#             'url': url,
#             'phone_numbers': phone_numbers
#         }
        
#         # Start automation in background
#         task = asyncio.create_task(run_automation(task_id, config))
#         active_tasks[task_id] = {
#             'task': task,
#             'progress': 0,
#             'status': 'running',
#             'message': 'Starting automation...',
#             'temp_dir': temp_dir,
#             'zip_file': None,
#             'agent_id': agent_id
#         }
        
#         print(f"Task {task_id} started successfully")
#         return {"task_id": task_id, "success": True}
        
#     except Exception as e:
#         print(f"Error in FIXED automation endpoint: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# @app.get("/api/automation/{task_id}/status")
# async def get_automation_status(task_id: str):
#     if task_id not in active_tasks:
#         raise HTTPException(status_code=404, detail="Task not found")
    
#     task_info = active_tasks[task_id]
#     return {
#         "progress": task_info['progress'],
#         "status": task_info['status'],
#         "message": task_info['message']
#     }

# @app.get("/api/automation/{task_id}/download")
# async def download_automation_result(task_id: str):
#     if task_id not in active_tasks:
#         raise HTTPException(status_code=404, detail="Task not found")
    
#     task_info = active_tasks[task_id]
    
#     if task_info['status'] != 'completed':
#         raise HTTPException(status_code=400, detail="Task not completed yet")
    
#     if not task_info['zip_file'] or not os.path.exists(task_info['zip_file']):
#         raise HTTPException(status_code=404, detail="Download file not found")
    
#     # Get agent info for filename
#     agent_id = task_info.get('agent_id', 'unknown')
#     timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#     filename = f"livevox_calls_{agent_id}_{timestamp}.zip"
    
#     def cleanup_files():
#         """Clean up temp files after download"""
#         try:
#             if os.path.exists(task_info['zip_file']):
#                 os.remove(task_info['zip_file'])
#             if os.path.exists(task_info['temp_dir']):
#                 shutil.rmtree(task_info['temp_dir'])
#             del active_tasks[task_id]
#         except Exception as e:
#             print(f"Error cleaning up files for task {task_id}: {e}")
    
#     # Schedule cleanup after a delay (gives time for download to complete)
#     threading.Timer(60.0, cleanup_files).start()
    
#     return FileResponse(
#         task_info['zip_file'],
#         filename=filename,
#         media_type="application/zip"
#     )

# async def run_automation(task_id: str, config: Dict[str, Any]):
#     import time
#     start_time = time.time()
#     timeout_minutes = 30  # 30 minute timeout
    
#     try:
#         # Update progress function
#         def update_progress(progress: int, message: str):
#             if task_id in active_tasks:
#                 elapsed = int((time.time() - start_time) / 60)
#                 active_tasks[task_id]['progress'] = progress
#                 active_tasks[task_id]['message'] = f"{message} (Running {elapsed}m)"
                
#                 # Check for timeout
#                 if elapsed >= timeout_minutes:
#                     raise Exception(f"Automation timeout after {timeout_minutes} minutes")
        
#         update_progress(5, "Starting browser...")
        
#         async with async_playwright() as playwright:
#             browser = await playwright.webkit.launch()
#             context = await browser.new_context(accept_downloads=True)
#             page = await context.new_page()
#             await page.set_viewport_size({"width": 1440, "height": 1440})
#             page.set_default_timeout(30000)
            
#             # Add page error listener for debugging
#             def handle_page_error(error):
#                 print(f"Page error: {error}")
#             page.on("pageerror", handle_page_error)
            
#             try:
#                 # Login with proper waits
#                 update_progress(10, "Logging in...")
#                 await page.goto(config['url'])
#                 await page.locator("#username").fill(config['username'])
#                 await page.locator("#password").fill(config['password'])
#                 await page.locator("#password").press("Enter")
                
#                 # Wait for login to complete and page to be fully loaded
#                 update_progress(12, "Waiting for login to complete...")
#                 await page.wait_for_load_state("networkidle")
#                 await asyncio.sleep(3)  # Additional wait for page stabilization
                
#                 # Verify we're logged in by waiting for a dashboard element
#                 update_progress(14, "Verifying login success...")
#                 try:
#                     # Check current URL and page state
#                     current_url = page.url
#                     print(f"Current URL after login: {current_url}")
                    
#                     # Wait for any element that indicates successful login
#                     await page.wait_for_selector("button:has-text('Review')", timeout=15000)
#                     update_progress(15, "Login verified - Review button found")
#                 except Exception as e:
#                     # If Review button not found, try waiting for other common elements
#                     update_progress(14, "Review button not immediately found, waiting longer...")
#                     await page.wait_for_load_state("domcontentloaded")
#                     await asyncio.sleep(2)
                    
#                     # Check if we might be on a wrong page or login failed
#                     page_title = await page.title()
#                     print(f"Page title: {page_title}")
#                     if "login" in page_title.lower() or "sign" in page_title.lower():
#                         raise Exception("Login may have failed - still on login page")
                
#                 if config['function_type'] == 'specific_calls':
#                     await run_specific_calls_logic(page, config, update_progress)
#                 elif config['function_type'] == 'all_calls':
#                     await run_all_calls_logic(page, config, update_progress)
                
#                 # Create ZIP file after automation completes
#                 update_progress(95, "Creating ZIP file...")
#                 zip_file_path = await create_zip_file(task_id, config['temp_dir'], config['agent_id'])
                
#                 if task_id in active_tasks:
#                     active_tasks[task_id]['zip_file'] = zip_file_path
#                     active_tasks[task_id]['agent_id'] = config['agent_id']
                
#                 elapsed = int((time.time() - start_time) / 60)
#                 update_progress(100, f"Automation completed successfully in {elapsed}m! ZIP file ready for download.")
#                 active_tasks[task_id]['status'] = 'completed'
                
#             except Exception as e:
#                 error_msg = str(e)
#                 if "timeout" in error_msg.lower():
#                     update_progress(0, f"Automation timed out: {error_msg}")
#                 else:
#                     update_progress(0, f"Error: {error_msg}")
#                 active_tasks[task_id]['status'] = 'failed'
#             finally:
#                 await browser.close()
                
#     except Exception as e:
#         if task_id in active_tasks:
#             active_tasks[task_id]['status'] = 'failed'
#             active_tasks[task_id]['message'] = f"Error: {str(e)}"

# async def create_zip_file(task_id: str, temp_dir: str, agent_id: str) -> str:
#     """Create a ZIP file containing all downloaded files"""
#     timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#     zip_filename = f"livevox_calls_{agent_id}_{timestamp}.zip"
#     zip_path = os.path.join(tempfile.gettempdir(), zip_filename)
    
#     file_count = 0
#     with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
#         for root, dirs, files in os.walk(temp_dir):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 # Add file to ZIP with relative path
#                 arcname = os.path.relpath(file_path, temp_dir)
#                 zipf.write(file_path, arcname)
#                 file_count += 1
    
#     print(f"Created ZIP file: {zip_path} with {file_count} files")
#     return zip_path

# async def run_specific_calls_logic(page, config, update_progress):
#     """Implementation for Specific Calls automation logic"""
#     agent_details_map = {
#         "3P_95": {"folder": "Chuck", "locator_id": "963665"},
#         "3P_235": {"folder": "Jim", "locator_id": "976426"},
#         "3P_1483": {"folder": "Clifford", "locator_id": "969789"},
#         "3P_260": {"folder": "Kathy", "locator_id": "963666"},
#         "3P_282": {"folder": "Laurie", "locator_id": "924766"}
#     }
    
#     current_agent_id = config['agent_id']
#     agent_info = agent_details_map.get(current_agent_id)
    
#     if not agent_info:
#         raise Exception(f"Agent ID '{current_agent_id}' not found in mapping")
    
#     calls_to_process = data_manager.get_calls(current_agent_id)
#     if not calls_to_process:
#         raise Exception(f"No calls configured for agent '{current_agent_id}'")
    
#     # Use temp directory instead of user-specified output directory
#     target_dir = os.path.join(config['temp_dir'], agent_info['folder'])
#     os.makedirs(target_dir, exist_ok=True)
    
#     update_progress(15, f"Starting automation for {len(calls_to_process)} calls for {agent_info['folder']}")
    
#     download_counter = 1
    
#     # Navigate to reports with better error handling
#     update_progress(18, "Navigating to Call Recording Report...")
#     try:
#         # Wait for and click Review button
#         await page.wait_for_selector("button:has-text('Review')", timeout=30000)
#         await page.get_by_role("button", name="Review").click()
        
#         # Wait for Agent Reports to appear and click it
#         await page.wait_for_selector("text=Agent Reports", timeout=15000)
#         await page.get_by_text("Agent Reports").click()
        
#         # Wait for Call Recording Report to appear
#         update_progress(19, "Waiting for Call Recording Report...")
#         await page.wait_for_selector("div.MuiTreeItem-label:has-text('Call Recording Report')", timeout=60000)
#         await page.locator("div.MuiTreeItem-label").filter(has_text="Call Recording Report").click()
        
#         # Wait for the report page to fully load
#         await page.wait_for_load_state("networkidle")
#         update_progress(20, "Report page loaded successfully")
        
#     except Exception as nav_error:
#         raise Exception(f"Navigation failed: {str(nav_error)}. Make sure you're logged into the correct LiveVox portal.")
    
#     # Set date and agent
#     update_progress(22, f"Setting up search for agent {current_agent_id}")
#     await page.locator("#search-panel__start-date").fill(config['start_date'])
    
#     # Click agent dropdown
#     await page.get_by_role("row", name="Agent Select One ... Result").locator("u").click()
#     await page.get_by_placeholder("Search...").fill(current_agent_id)
    
#     # Select the specific agent
#     agent_selector = f'[id="\\33 {agent_info["locator_id"]}"]'
#     try:
#         await page.wait_for_selector(agent_selector, timeout=10000)
#         await page.locator(agent_selector).click()
#         await page.locator("#agent-combo__ok-btn").click()
#         update_progress(24, f"Agent {current_agent_id} selected successfully")
#     except Exception as e:
#         raise Exception(f"Could not find agent {current_agent_id} (locator: {agent_info['locator_id']}). Check agent mapping.")
    
#     # Process each call
#     for i, call_data in enumerate(calls_to_process):
#         progress = 25 + int(((i + 1) / len(calls_to_process)) * 65)
#         update_progress(progress, f"Searching call {i+1}/{len(calls_to_process)}: {call_data['phone']} (duration: {call_data['duration']}s)")
        
#         await page.locator("#search-panel__phone-dialed").clear()
#         await page.locator("#search-panel__phone-dialed").fill(call_data['phone'])
#         await page.get_by_role("button", name="Generate Report").click()
        
#         try:
#             results_table_body = page.locator("div.rt-tbody")
#             first_row = results_table_body.locator("div.rt-tr:not(.-padRow)").first
#             await first_row.wait_for(state="visible", timeout=15000)
            
#             data_rows = await results_table_body.locator("div.rt-tr:not(.-padRow)").all()
#             update_progress(progress, f"Found {len(data_rows)} recordings for {call_data['phone']}, checking durations...")
            
#             found_match = False
#             for j, row in enumerate(data_rows):
#                 duration_in_row = await row.locator("div.rt-td").nth(8).inner_text()
#                 if duration_in_row == call_data['duration']:
#                     update_progress(progress, f"Found matching duration {duration_in_row}s, downloading...")
#                     download_button = row.locator("div.icon--audio-download.clickable")
#                     async with page.expect_download() as download_info:
#                         await download_button.click()
                    
#                     download = await download_info.value
#                     base_filename = download.suggested_filename
#                     name, ext = os.path.splitext(base_filename)
                    
#                     final_filename = f"{name}-{download_counter}{ext}"
#                     target_path = os.path.join(target_dir, final_filename)
                    
#                     update_progress(progress, f"Saved: {final_filename}")
#                     shutil.move(await download.path(), target_path)
                    
#                     download_counter += 1
#                     found_match = True
#                     break
            
#             if not found_match:
#                 update_progress(progress, f"No matching duration found for {call_data['phone']} (needed: {call_data['duration']}s)")
                    
#         except Exception as e:
#             update_progress(progress, f"No results found for {call_data['phone']}: {str(e)[:50]}")
    
#     update_progress(90, f"Completed processing {len(calls_to_process)} calls. Downloaded {download_counter-1} files.")

# async def run_all_calls_logic(page, config, update_progress):
#     """Implementation for All Calls automation logic"""
#     agent_details_map = {
#         "3P_95": {"folder": "Chuck", "locator_id": "963665"},
#         "3P_235": {"folder": "Jim", "locator_id": "976426"},
#         "3P_1483": {"folder": "Clifford", "locator_id": "969789"},
#         "3P_260": {"folder": "Kathy", "locator_id": "963666"},
#         "3P_282": {"folder": "Laurie", "locator_id": "924766"}
#     }
    
#     current_agent_id = config['agent_id']
#     agent_info = agent_details_map.get(current_agent_id)
    
#     if not agent_info:
#         raise Exception(f"Agent ID '{current_agent_id}' not found in mapping")
    
#     phone_numbers = config['phone_numbers'].split(',')
#     phone_numbers = [phone.strip() for phone in phone_numbers if phone.strip()]
    
#     if not phone_numbers:
#         raise Exception("No valid phone numbers provided")
    
#     # Use temp directory instead of user-specified output directory
#     target_dir = os.path.join(config['temp_dir'], agent_info['folder'])
#     os.makedirs(target_dir, exist_ok=True)
    
#     update_progress(15, f"Processing {len(phone_numbers)} phone numbers for {agent_info['folder']}")
    
#     download_counter = 1
    
#     # Navigate to reports with better error handling
#     update_progress(18, "Navigating to Call Recording Report...")
#     try:
#         # Wait for and click Review button
#         await page.wait_for_selector("button:has-text('Review')", timeout=30000)
#         await page.get_by_role("button", name="Review").click()
        
#         # Wait for Agent Reports to appear and click it
#         await page.wait_for_selector("text=Agent Reports", timeout=15000)
#         await page.get_by_text("Agent Reports").click()
        
#         # Wait for Call Recording Report to appear
#         update_progress(19, "Waiting for Call Recording Report...")
#         await page.wait_for_selector("div.MuiTreeItem-label:has-text('Call Recording Report')", timeout=60000)
#         await page.locator("div.MuiTreeItem-label").filter(has_text="Call Recording Report").click()
        
#         # Wait for the report page to fully load
#         await page.wait_for_load_state("networkidle")
#         update_progress(20, "Report page loaded successfully")
        
#     except Exception as nav_error:
#         raise Exception(f"Navigation failed: {str(nav_error)}. Make sure you're logged into the correct LiveVox portal.")
    
#     # Set date and agent  
#     update_progress(22, f"Setting up search for agent {current_agent_id}")
#     await page.locator("#search-panel__start-date").fill(config['start_date'])
    
#     # Click agent dropdown
#     await page.get_by_role("row", name="Agent Select One ... Result").locator("u").click()
#     await page.get_by_placeholder("Search...").fill(current_agent_id)
    
#     # Select the specific agent
#     agent_selector = f'[id="\\33 {agent_info["locator_id"]}"]'
#     try:
#         await page.wait_for_selector(agent_selector, timeout=10000)
#         await page.locator(agent_selector).click()
#         await page.locator("#agent-combo__ok-btn").click()
#         update_progress(24, f"Agent {current_agent_id} selected successfully")
#     except Exception as e:
#         raise Exception(f"Could not find agent {current_agent_id} (locator: {agent_info['locator_id']}). Check agent mapping.")
    
#     # Process each phone number
#     for i, phone in enumerate(phone_numbers):
#         progress = 25 + int(((i + 1) / len(phone_numbers)) * 65)
#         update_progress(progress, f"Processing phone {i+1}/{len(phone_numbers)}: {phone}")
        
#         await page.locator("#search-panel__phone-dialed").clear()
#         await page.locator("#search-panel__phone-dialed").fill(phone)
#         await page.get_by_role("button", name="Generate Report").click()
        
#         try:
#             results_table_body = page.locator("div.rt-tbody")
#             first_row = results_table_body.locator("div.rt-tr:not(.-padRow)").first
#             await first_row.wait_for(state="visible", timeout=15000)
            
#             data_rows = await results_table_body.locator("div.rt-tr:not(.-padRow)").all()
            
#             update_progress(progress, f"Found {len(data_rows)} recording(s) for phone {phone}. Downloading all...")
            
#             for row in data_rows:
#                 download_button = row.locator("div.icon--audio-download.clickable")
#                 async with page.expect_download() as download_info:
#                     await download_button.click()
                
#                 download = await download_info.value
#                 base_filename = download.suggested_filename
#                 name, ext = os.path.splitext(base_filename)
                
#                 final_filename = f"{name}-{download_counter}{ext}"
#                 target_path = os.path.join(target_dir, final_filename)
                
#                 update_progress(progress, f"Saving file: {final_filename}")
#                 shutil.move(await download.path(), target_path)
                
#                 download_counter += 1
                
#         except Exception as e:
#             update_progress(progress, f"No recordings found for phone: {phone}")
    
#     update_progress(90, f"Completed processing {len(phone_numbers)} phone numbers. Downloaded {download_counter-1} files.")

# if __name__ == "__main__":
#     # Create templates directory if it doesn't exist
#     os.makedirs("templates", exist_ok=True)
#     uvicorn.run(app, host="0.0.0.0", port=8001)


from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
import uvicorn
import os
import json
import asyncio
from typing import Optional, List, Dict, Any
import pandas as pd
from datetime import datetime, timedelta
import threading
import time
from playwright.async_api import async_playwright
import shutil
import uuid
import tempfile
import zipfile
import logging
import glob
import re
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend before importing pyplot
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.drawing.image import Image as OpenpyxlImage

# Initialize FastAPI
app = FastAPI(title="Multi-Project Automation Hub")

# Templates
templates = Jinja2Templates(directory="templates")

print("Server starting...")
print("Available imports:")
print("- FastAPI:", FastAPI.__version__ if hasattr(FastAPI, '__version__') else "imported")
print("- Playwright: imported")
print("- Pandas:", pd.__version__)
print("- All other dependencies: imported")

class DataManager:
    """Manages agent and call data using local JSON storage"""
    def __init__(self, project_name="livevox"):
        self.project_name = project_name
        self.local_file = f"{project_name}_data.json"
        print(f"Using local storage: {self.local_file}")
    
    def load_data(self):
        """Load data from local JSON file"""
        if os.path.exists(self.local_file):
            try:
                with open(self.local_file, 'r') as f:
                    data = json.load(f)
                    print(f"Loaded data from {self.local_file}")
                    return data
            except Exception as e:
                print(f"Error loading {self.local_file}: {e}")
        
        # Return default structure if file doesn't exist
        default_data = {"agents": {}, "calls": {}}
        self.save_data(default_data)
        return default_data
    
    def save_data(self, data):
        """Save data to local JSON file"""
        try:
            with open(self.local_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Data saved to {self.local_file}")
            return True
        except Exception as e:
            print(f"Error saving to {self.local_file}: {e}")
            return False
    
    def add_agent(self, agent_data):
        data = self.load_data()
        agent_id = agent_data['id']
        data['agents'][agent_id] = agent_data
        if agent_id not in data['calls']:
            data['calls'][agent_id] = []
        self.save_data(data)
    
    def remove_agent(self, agent_id):
        data = self.load_data()
        if agent_id in data['agents']:
            del data['agents'][agent_id]
        if agent_id in data['calls']:
            del data['calls'][agent_id]
        self.save_data(data)

    def remove_all_agents(self):
        data = {"agents": {}, "calls": {}}
        self.save_data(data)
    
    def add_call(self, agent_id, call_data):
        data = self.load_data()
        if agent_id not in data['calls']:
            data['calls'][agent_id] = []
        data['calls'][agent_id].append(call_data)
        self.save_data(data)
    
    def remove_all_calls(self, agent_id):
        data = self.load_data()
        if agent_id in data['calls']:
            data['calls'][agent_id] = []
            self.save_data(data)
    
    def remove_call(self, agent_id, call_index):
        data = self.load_data()
        if agent_id in data['calls'] and 0 <= call_index < len(data['calls'][agent_id]):
            del data['calls'][agent_id][call_index]
            self.save_data(data)
    
    def get_agents(self):
        return self.load_data()['agents']
    
    def get_calls(self, agent_id):
        return self.load_data()['calls'].get(agent_id, [])

class HciDataManager(DataManager):
    """Manages HCI agent data using local JSON storage"""
    def __init__(self):
        super().__init__("hci")
    
    def load_data(self):
        """Load data from local JSON file with default HCI agents"""
        if os.path.exists(self.local_file):
            try:
                with open(self.local_file, 'r') as f:
                    data = json.load(f)
                    print(f"Loaded HCI data from {self.local_file}")
                    return data
            except Exception as e:
                print(f"Error loading {self.local_file}: {e}")
        
        # Return default structure with default HCI agents if file doesn't exist
        default_data = {"agents": HCI_AGENT_LIST.copy()}
        self.save_data(default_data)
        return default_data

# Global data managers
data_manager = DataManager()
hci_data_manager = HciDataManager()

# HCI Configuration
HCI_AGENT_LIST = [
    'JCI_HCI_AGENT (3181894)',
    'BN_HCI_AGENT (3176615)',
    'AU_HCI_AGENT (3174939)',
    'DS_HCI_AGENT (3173370)',
    'FEDEX_HCI_AGENT (3175378)',
    'LB1_HCI_AGENT (3183640)',
    'LB2_HCI_AGENT (3174416)',
    'SW_HCI_AGENT (3174210)',
    'LARGE_BAL_HCI_AGENT (3179837)',
    'PHI_HCI_AGENT (3191012)',
    'SMALL_BAL_HCI_AGENT (3179861)',
    'DELL_HCI_AGENT (3184975)',
    'ATI_RESTORATION_HCI_AGENT',
    'DS_DRAGON_HCI_AGENT',
    'DOM_HCI_AGENT_Uline (3186839)',
    'DOM_HCI_AGENT_SB_Team (3187140)',
]

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/livevox", response_class=HTMLResponse)
async def livevox_app(request: Request):
    agents = data_manager.get_agents()
    return templates.TemplateResponse("livevox.html", {
        "request": request, 
        "agents": agents
    })

@app.get("/hci-summary", response_class=HTMLResponse)
async def hci_summary_app(request: Request):
    return templates.TemplateResponse("hci_summary.html", {"request": request})

# Store active automation tasks with their temp directories and results
active_tasks = {}

# Existing LiveVox automation endpoints (keeping all existing ones)
@app.post("/api/agents")
async def create_agent(agent_id: str = Form(...), folder: str = Form(...), locator_id: str = Form(...)):
    if agent_id in data_manager.get_agents():
        raise HTTPException(status_code=400, detail="Agent ID already exists")
    
    agent_data = {
        'id': agent_id,
        'folder': folder,
        'locator_id': locator_id
    }
    data_manager.add_agent(agent_data)
    return {"success": True}

@app.get("/api/agents")
async def get_agents():
    return data_manager.get_agents()

@app.put("/api/agents/{agent_id}")
async def update_agent(agent_id: str, agent_id_field: str = Form(..., alias="agent_id"), folder: str = Form(...), locator_id: str = Form(...)):
    print(f"PUT /api/agents/{agent_id} called with data: agent_id={agent_id_field}, folder={folder}, locator_id={locator_id}")
    
    try:
        data = data_manager.load_data()
        
        if agent_id not in data['agents']:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        if agent_id != agent_id_field:
            if agent_id_field in data['agents']:
                raise HTTPException(status_code=400, detail="New Agent ID already exists")
            
            data['agents'][agent_id_field] = {
                'id': agent_id_field,
                'folder': folder,
                'locator_id': locator_id
            }
            del data['agents'][agent_id]
            
            if agent_id in data['calls']:
                data['calls'][agent_id_field] = data['calls'][agent_id]
                del data['calls'][agent_id]
        else:
            data['agents'][agent_id] = {
                'id': agent_id_field,
                'folder': folder,
                'locator_id': locator_id
            }
        
        data_manager.save_data(data)
        print(f"Agent updated successfully: {agent_id} -> {agent_id_field}")
        return {"success": True, "new_agent_id": agent_id_field}
        
    except Exception as e:
        print(f"Error updating agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/agents/{agent_id}")
async def delete_agent(agent_id: str):
    data_manager.remove_agent(agent_id)
    return {"success": True}

@app.post("/api/agents/{agent_id}/calls")
async def add_call(agent_id: str, phone: str = Form(...), duration: str = Form(...)):
    call_data = {'phone': phone, 'duration': duration}
    data_manager.add_call(agent_id, call_data)
    return {"success": True}

@app.get("/api/agents/{agent_id}/calls")
async def get_calls(agent_id: str):
    return data_manager.get_calls(agent_id)

@app.put("/api/agents/{agent_id}/calls/{call_index}")
async def update_call(agent_id: str, call_index: int, phone: str = Form(...), duration: str = Form(...)):
    print(f"PUT /api/agents/{agent_id}/calls/{call_index} called with phone={phone}, duration={duration}")
    
    try:
        data = data_manager.load_data()
        
        if agent_id not in data['calls']:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        if call_index >= len(data['calls'][agent_id]) or call_index < 0:
            raise HTTPException(status_code=404, detail="Call not found")
        
        data['calls'][agent_id][call_index] = {'phone': phone, 'duration': duration}
        data_manager.save_data(data)
        print(f"Call updated successfully: agent={agent_id}, index={call_index}")
        return {"success": True}
        
    except Exception as e:
        print(f"Error updating call: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/agents/{agent_id}/calls/{call_index}")
async def delete_call(agent_id: str, call_index: int):
    data_manager.remove_call(agent_id, call_index)
    return {"success": True}

@app.post("/api/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        
        temp_path = f"temp_{uuid.uuid4().hex}.xlsx"
        with open(temp_path, "wb") as f:
            f.write(contents)
        
        df = pd.read_excel(temp_path, dtype=str)
        os.remove(temp_path)
        
        required_cols = {'phone number', 'duration', 'agent ID', 'folder name (name)', 'locator'}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            raise HTTPException(status_code=400, detail=f"Missing columns: {', '.join(missing)}")
        
        agents_created = 0
        calls_added = 0
        
        for _, row in df.iterrows():
            agent_id = str(row.get('agent ID', '')).strip()
            folder = str(row.get('folder name (name)', '')).strip()
            locator = str(row.get('locator', '')).strip()
            phone = str(row.get('phone number', '')).strip()
            duration = str(row.get('duration', '')).strip()
            
            if not all([agent_id, folder, locator, phone, duration]):
                continue
            
            if agent_id not in data_manager.get_agents():
                agent_data = {
                    'id': agent_id,
                    'folder': folder,
                    'locator_id': locator
                }
                data_manager.add_agent(agent_data)
                agents_created += 1
            
            call_data = {'phone': phone, 'duration': duration}
            data_manager.add_call(agent_id, call_data)
            calls_added += 1
        
        return {
            "success": True,
            "agents_created": agents_created,
            "calls_added": calls_added
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download-template")
async def download_template():
    template_data = {
        'phone number': ['7021234567', '7029876543'],
        'duration': [65, 123],
        'agent ID': ['3P_95', '3P_235'],
        'folder name (name)': ['Chuck', 'Jim'],
        'locator': ['963665', '976426']
    }
    df = pd.DataFrame(template_data)
    
    filename = "call_upload_template.xlsx"
    df.to_excel(filename, index=False)
    
    return FileResponse(
        filename,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.delete("/api/agents")
async def delete_all_agents():
    data_manager.remove_all_agents()
    return {"success": True}

@app.delete("/api/agents/{agent_id}/calls")
async def delete_all_calls_for_agent(agent_id: str):
    data_manager.remove_all_calls(agent_id)
    return {"success": True}

# Existing LiveVox automation endpoint
@app.post("/api/automation/start")
async def start_automation_fixed(
    function_type: str = Form(...),
    agent_id: str = Form(...),
    start_date: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    url: str = Form(...),
    phone_numbers: Optional[str] = Form(None)
):
    """FIXED: No output_dir required anymore - uses temp directories"""
    try:
        print("=" * 50)
        print("FIXED AUTOMATION ENDPOINT CALLED")
        print(f"Function parameters received:")
        print(f"  function_type: {function_type}")
        print(f"  agent_id: {agent_id}")
        print(f"  start_date: {start_date}")
        print(f"  username: {username}")
        print(f"  url: {url}")
        print(f"  phone_numbers: {phone_numbers}")
        print("=" * 50)
        
        task_id = str(uuid.uuid4())
        
        temp_dir = tempfile.mkdtemp(prefix=f"livevox_{task_id}_")
        print(f"Created temp directory: {temp_dir}")
        
        config = {
            'function_type': function_type,
            'agent_id': agent_id,
            'start_date': start_date,
            'temp_dir': temp_dir,
            'username': username,
            'password': password,
            'url': url,
            'phone_numbers': phone_numbers
        }
        
        task = asyncio.create_task(run_automation(task_id, config))
        active_tasks[task_id] = {
            'task': task,
            'progress': 0,
            'status': 'running',
            'message': 'Starting automation...',
            'temp_dir': temp_dir,
            'zip_file': None,
            'agent_id': agent_id
        }
        
        print(f"Task {task_id} started successfully")
        return {"task_id": task_id, "success": True}
        
    except Exception as e:
        print(f"Error in FIXED automation endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# NEW HCI Summary Report Endpoints
@app.post("/api/hci/automation/start")
async def start_hci_automation(
    username: str = Form(...),
    password: str = Form(...),
    url: str = Form(...),
    selected_agents: str = Form(...),  # Comma-separated list of selected agents
    report_date: Optional[str] = Form(None)  # Add this parameter
):
    """Start HCI Summary Report automation"""
    try:
        print("=" * 50)
        print("HCI AUTOMATION ENDPOINT CALLED")
        print(f"Username: {username}")
        print(f"URL: {url}")
        print(f"Selected agents: {selected_agents}")
        print(f"Report date: {report_date}")  # Add this log
        print("=" * 50)
        
        task_id = str(uuid.uuid4())
        
        temp_dir = tempfile.mkdtemp(prefix=f"hci_{task_id}_")
        print(f"Created temp directory: {temp_dir}")
        
        # Parse selected agents
        selected_agent_list = [agent.strip() for agent in selected_agents.split(',') if agent.strip()]
        
        config = {
            'username': username,
            'password': password,
            'url': url,
            'selected_agents': selected_agent_list,
            'temp_dir': temp_dir,
            'report_date': report_date  # Add this to config
        }
        
        task = asyncio.create_task(run_hci_automation(task_id, config))
        active_tasks[task_id] = {
            'task': task,
            'progress': 0,
            'status': 'running',
            'message': 'Starting HCI automation...',
            'temp_dir': temp_dir,
            'zip_file': None,
            'project_type': 'hci'
        }
        
        print(f"HCI Task {task_id} started successfully")
        return {"task_id": task_id, "success": True}
        
    except Exception as e:
        print(f"Error in HCI automation endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/api/hci/agents")
async def get_hci_agents():
    """Get list of available HCI agents"""
    return {"agents": hci_data_manager.load_data().get('agents', HCI_AGENT_LIST)}

@app.post("/api/hci/agents")
async def add_hci_agent(request: Request):
    """Add a new HCI agent"""
    try:
        body = await request.json()
        agent_name = body.get('agent_name')
        
        if not agent_name:
            raise HTTPException(status_code=400, detail="Agent name is required")
        
        data = hci_data_manager.load_data()
        if 'agents' not in data:
            data['agents'] = HCI_AGENT_LIST.copy()
        
        if agent_name in data['agents']:
            raise HTTPException(status_code=400, detail="Agent already exists")
        
        data['agents'].append(agent_name)
        hci_data_manager.save_data(data)
        
        return {"success": True, "message": f"Agent '{agent_name}' added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/hci/agents")
async def remove_hci_agent(request: Request):
    """Remove an HCI agent"""
    try:
        body = await request.json()
        agent_name = body.get('agent_name')
        
        if not agent_name:
            raise HTTPException(status_code=400, detail="Agent name is required")
        
        data = hci_data_manager.load_data()
        if 'agents' not in data:
            data['agents'] = HCI_AGENT_LIST.copy()
        
        if agent_name not in data['agents']:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        data['agents'].remove(agent_name)
        hci_data_manager.save_data(data)
        
        return {"success": True, "message": f"Agent '{agent_name}' removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/automation/{task_id}/status")
async def get_automation_status(task_id: str):
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_info = active_tasks[task_id]
    return {
        "progress": task_info['progress'],
        "status": task_info['status'],
        "message": task_info['message']
    }

@app.get("/api/automation/{task_id}/download")
async def download_automation_result(task_id: str):
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_info = active_tasks[task_id]
    
    if task_info['status'] != 'completed':
        raise HTTPException(status_code=400, detail="Task not completed yet")
    
    if not task_info['zip_file'] or not os.path.exists(task_info['zip_file']):
        raise HTTPException(status_code=404, detail="Download file not found")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    project_type = task_info.get('project_type', 'livevox')
    
    if project_type == 'hci':
        filename = f"hci_summary_report_{timestamp}.zip"
    else:
        agent_id = task_info.get('agent_id', 'unknown')
        filename = f"livevox_calls_{agent_id}_{timestamp}.zip"
    
    def cleanup_files():
        """Clean up temp files after download"""
        try:
            if os.path.exists(task_info['zip_file']):
                os.remove(task_info['zip_file'])
            if os.path.exists(task_info['temp_dir']):
                shutil.rmtree(task_info['temp_dir'])
            del active_tasks[task_id]
        except Exception as e:
            print(f"Error cleaning up files for task {task_id}: {e}")
    
    threading.Timer(60.0, cleanup_files).start()
    
    return FileResponse(
        task_info['zip_file'],
        filename=filename,
        media_type="application/zip"
    )

@app.post("/api/automation/{task_id}/stop")
async def stop_automation(task_id: str):
    """Stop a running automation task"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        task_info = active_tasks[task_id]
        
        # Cancel the asyncio task (this will terminate Playwright)
        if 'task' in task_info and not task_info['task'].done():
            task_info['task'].cancel()
            
            # Wait a bit for graceful cancellation
            try:
                await asyncio.wait_for(task_info['task'], timeout=5.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass  # Expected when cancelling
        
        # Update task status
        task_info['status'] = 'stopped'
        task_info['message'] = 'Automation stopped by user'
        task_info['progress'] = 0
        
        # Clean up temp directory if it exists
        if 'temp_dir' in task_info and os.path.exists(task_info['temp_dir']):
            try:
                shutil.rmtree(task_info['temp_dir'])
            except Exception as cleanup_error:
                print(f"Error cleaning up temp dir: {cleanup_error}")
        
        print(f"Successfully stopped task {task_id}")
        return {"success": True, "message": "Automation stopped successfully"}
        
    except Exception as e:
        print(f"Error stopping task {task_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error stopping automation: {str(e)}")

# HCI Automation Functions
async def run_hci_automation(task_id: str, config: Dict[str, Any]):
    """Run HCI Summary Report automation using Playwright"""
    import time
    start_time = time.time()
    timeout_minutes = 45  # 45 minute timeout for HCI
    
    try:
        def update_progress(progress: int, message: str):
            if task_id in active_tasks:
                elapsed = int((time.time() - start_time) / 60)
                active_tasks[task_id]['progress'] = progress
                active_tasks[task_id]['message'] = f"{message} (Running {elapsed}m)"
                
                if elapsed >= timeout_minutes:
                    raise Exception(f"HCI automation timeout after {timeout_minutes} minutes")
        
        # Check for cancellation at key points
        if asyncio.current_task().cancelled():
            raise asyncio.CancelledError("Task was cancelled")
            
        update_progress(5, "Starting browser...")
        
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            
            context = await browser.new_context(
                accept_downloads=True,
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            page.set_default_timeout(30000)
            
            def handle_page_error(error):
                print(f"Page error: {error}")
            page.on("pageerror", handle_page_error)
            
            try:
                # Check for cancellation
                if asyncio.current_task().cancelled():
                    raise asyncio.CancelledError("Task was cancelled")
                    
                update_progress(10, "Logging into LiveVox...")
                
                await page.goto(config['url'])
                await page.wait_for_selector("#username", timeout=30000)
                await page.fill("#username", config['username'])
                await page.fill("#password", config['password'])
                await page.click("#loginBtn span")
                
                update_progress(15, "Login successful, navigating to reports...")
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(3)
                
                # Check for cancellation
                if asyncio.current_task().cancelled():
                    raise asyncio.CancelledError("Task was cancelled")
                
                # Navigate to Review > Agent Reports > Agent Summary
                update_progress(16, "Clicking Review...")
                await page.wait_for_selector("#lv-app div aside div div div:nth-child(2) ul button:nth-child(3)", timeout=30000)
                await page.click("#lv-app div aside div div div:nth-child(2) ul button:nth-child(3)")
                
                update_progress(17, "Opening Agent Reports...")
                await page.wait_for_selector("#acdReports div", timeout=30000)
                await page.click("#acdReports div")
                
                update_progress(18, "Opening Agent Summary Report...")
                await page.wait_for_selector('[id="11"]', timeout=30000)
                await page.click('[id="11"]')
                
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(2)
                
                # FIXED: Use the provided date or default to yesterday
                if config.get('report_date'):
                    # Parse the provided date (format: YYYY-MM-DD from HTML date input)
                    target_date = datetime.strptime(config['report_date'], '%Y-%m-%d')
                    update_progress(20, f"Using provided date: {config['report_date']}")
                else:
                    # Default to yesterday if no date provided
                    target_date = datetime.now() - timedelta(days=1)
                    update_progress(20, "Using yesterday's date (default)")
                
                target_date_str = target_date.strftime('%m/%d/%Y')
                update_progress(21, f"Setting dates to {target_date_str}...")
                
                await page.wait_for_selector('#search-panel__start-date', timeout=30000)
                await page.fill('#search-panel__start-date', target_date_str)
                await page.fill('#search-panel__end-date', target_date_str)
                
                # Check for cancellation
                if asyncio.current_task().cancelled():
                    raise asyncio.CancelledError("Task was cancelled")
                
                # Process each selected agent
                total_agents = len(config['selected_agents'])
                downloaded_files = 0
                
                for i, hci_agent in enumerate(config['selected_agents']):
                    # Check for cancellation at start of each agent
                    if asyncio.current_task().cancelled():
                        raise asyncio.CancelledError("Task was cancelled")
                        
                    progress = 25 + int(((i + 1) / total_agents) * 60)
                    update_progress(progress, f"Processing agent {i+1}/{total_agents}: {hci_agent}")
                    
                    try:
                        # Click and type into custom select elements (like original Selenium send_keys)
                        await page.wait_for_selector('#service_type_combo', timeout=15000)
                        await page.click('#service_type_combo')
                        await page.keyboard.type('Quick Connect (Auto)')
                        await page.keyboard.press('Enter')
                        await asyncio.sleep(1)
                        
                        # Same approach for service combo
                        await page.wait_for_selector('#service_combo', timeout=15000)
                        await page.click('#service_combo')
                        await page.keyboard.type(hci_agent)
                        await page.keyboard.press('Enter')
                        await asyncio.sleep(1)
                        
                        # Generate report
                        update_progress(progress, f"Generating report for {hci_agent}...")
                        await page.click('.lv-button__inside')
                        await asyncio.sleep(3)
                        
                        # Check for cancellation before export
                        if asyncio.current_task().cancelled():
                            raise asyncio.CancelledError("Task was cancelled")
                        
                        # Export to Excel
                        update_progress(progress, f"Checking export availability for {hci_agent}...")
                        try:
                            export_btn = page.locator("#search-panel__export-btn")
                            await export_btn.wait_for(state="visible", timeout=10000)
                            
                            # Check if button is available and not disabled
                            try:
                                # Check if button has disabled class or attribute
                                is_disabled = await export_btn.get_attribute('disabled') is not None
                                has_disabled_class = 'disabled' in (await export_btn.get_attribute('class') or '')
                                
                                if not is_disabled and not has_disabled_class:
                                    update_progress(progress, f"Downloading data for {hci_agent}...")
                                    await export_btn.click()
                                    await asyncio.sleep(1)
                                    
                                    excel_link = page.locator("div.dropdown-content a:has-text('Excel')")
                                    await excel_link.wait_for(state="visible", timeout=5000)
                                    
                                    async with page.expect_download() as download_info:
                                        await excel_link.click()
                                    
                                    download = await download_info.value
                                    
                                    target_date_file_str = target_date.strftime('%m_%d_%Y')
                                    agent_name_clean = hci_agent.split(' ')[0]
                                    new_name = f"{agent_name_clean}_{target_date_file_str}.xls"
                                    target_path = os.path.join(config['temp_dir'], new_name)
                                    
                                    await download.save_as(target_path)
                                    downloaded_files += 1
                                    update_progress(progress, f"✅ Downloaded: {new_name}")
                                    print(f"Successfully downloaded: {new_name}")
                                    
                                else:
                                    # Button is disabled - no data found for this agent
                                    progress_msg = f"❌ NO DATA FOUND for {hci_agent} (no activity on {target_date_str})"
                                    update_progress(progress, progress_msg)
                                    print(f"❌ NO DATA FOUND for {hci_agent} - no activity on {target_date_str}")
                                    
                            except Exception as button_check_error:
                                # Fallback: try to click anyway, might work
                                try:
                                    update_progress(progress, f"Attempting download for {hci_agent}...")
                                    await export_btn.click()
                                    await asyncio.sleep(1)
                                    
                                    excel_link = page.locator("div.dropdown-content a:has-text('Excel')")
                                    await excel_link.wait_for(state="visible", timeout=5000)
                                    
                                    async with page.expect_download() as download_info:
                                        await excel_link.click()
                                    
                                    download = await download_info.value
                                    
                                    target_date_file_str = target_date.strftime('%m_%d_%Y')
                                    agent_name_clean = hci_agent.split(' ')[0]
                                    new_name = f"{agent_name_clean}_{target_date_file_str}.xls"
                                    target_path = os.path.join(config['temp_dir'], new_name)
                                    
                                    await download.save_as(target_path)
                                    downloaded_files += 1
                                    update_progress(progress, f"✅ Downloaded: {new_name}")
                                    print(f"Successfully downloaded: {new_name}")
                                    
                                except Exception as fallback_error:
                                    progress_msg = f"❌ NO DATA FOUND for {hci_agent} (export button unavailable)"
                                    update_progress(progress, progress_msg)
                                    print(f"❌ NO DATA for {hci_agent}: {fallback_error}")
                                        
                        except Exception as export_error:
                            update_progress(progress, f"Export failed for {hci_agent}: {str(export_error)}")
                            print(f"Export error for {hci_agent}: {export_error}")
                            
                    except Exception as agent_error:
                        update_progress(progress, f"Agent processing failed for {hci_agent}: {str(agent_error)}")
                        print(f"Agent error for {hci_agent}: {agent_error}")
                        continue
                
                # Check for cancellation before processing
                if asyncio.current_task().cancelled():
                    raise asyncio.CancelledError("Task was cancelled")
                
                update_progress(85, f"Agent processing complete. Downloaded {downloaded_files} files. Processing data...")
                
                if downloaded_files == 0:
                    raise Exception(f"No files were downloaded. Check agent names and LiveVox permissions.")
                
                # Pass the target_date to process_hci_files
                await process_hci_files(config['temp_dir'], update_progress, target_date)
                
                update_progress(95, "Creating ZIP file...")
                zip_file_path = await create_zip_file(task_id, config['temp_dir'], "hci_summary")
                
                if task_id in active_tasks:
                    active_tasks[task_id]['zip_file'] = zip_file_path
                    active_tasks[task_id]['project_type'] = 'hci'
                
                elapsed = int((time.time() - start_time) / 60)
                update_progress(100, f"HCI automation completed successfully in {elapsed}m! ZIP file ready for download.")
                active_tasks[task_id]['status'] = 'completed'
                
            except asyncio.CancelledError:
                print(f"HCI Task {task_id} was cancelled, cleaning up...")
                raise
            except Exception as e:
                error_msg = str(e)
                if "timeout" in error_msg.lower():
                    update_progress(0, f"HCI automation timed out: {error_msg}")
                else:
                    update_progress(0, f"Error: {error_msg}")
                active_tasks[task_id]['status'] = 'failed'
            finally:
                # Ensure browser is always closed
                try:
                    await browser.close()
                except:
                    pass
                
    except asyncio.CancelledError:
        # Handle cancellation gracefully
        if task_id in active_tasks:
            active_tasks[task_id]['status'] = 'stopped'
            active_tasks[task_id]['message'] = 'Automation stopped by user'
        print(f"HCI Task {task_id} cancelled successfully")
        raise
    except Exception as e:
        if task_id in active_tasks:
            active_tasks[task_id]['status'] = 'failed'
            active_tasks[task_id]['message'] = f"Error: {str(e)}"

async def process_hci_files(temp_dir: str, update_progress, target_date: datetime):
    """Process HCI downloaded files EXACTLY like original process.py"""
    try:
        target_date_str = target_date.strftime('%m-%d-%Y')
        
        # Find all downloaded Excel files
        excel_files = glob.glob(os.path.join(temp_dir, '*.xls'))
        if not excel_files:
            raise Exception("No Excel files found to process")
        
        update_progress(87, f"Found {len(excel_files)} files to process...")
        
        # STEP 1: Replicate append_files() function exactly
        headers = ['Service', 'Total', 'Successful Op Transfer', 'Successful Transactional Email', 
                  'Successful Transactional SMS', 'In Call (Min)', 'In Call (%)', 'Ready (Min)', 
                  'Ready (%)', 'Wrapup (Min)', 'Wrapup (%)', 'Not Ready (Min)', 'Not Ready (%)', 
                  'RPC : Payment/PTP', 'RPC : No Payment/PTP', 'WPC', 'Non-Contacts', 'Total RPCs']
        
        def generate_service_name(file):
            """Exactly like original generate_service_name"""
            match = re.search(r'(\w+)_([A-Za-z0-9]+)_([A-Za-z0-9]+)', os.path.basename(file))
            if match:
                return '_'.join(match.groups())
            else:
                return os.path.basename(file)
        
        dfs = []
        for file in excel_files:
            try:
                # For .xls files, try xlrd first
                if file.endswith('.xls'):
                    try:
                        file_df = pd.read_excel(file, engine='xlrd', header=None, names=headers)
                    except:
                        print(f'Could not read .xls file {file} - xlrd dependency missing. Install with: pip install xlrd')
                        continue
                else:
                    file_df = pd.read_excel(file, header=None, names=headers)
                    
                file_df['Service'] = generate_service_name(file)
                dfs.append(file_df)
                print(f'Loaded file: {file}')
            except Exception as e:
                print(f'Error reading file {file}: {e}')
                continue
        
        if not dfs:
            raise Exception("No files could be processed")
            
        # Concatenate all dataframes like original
        df = pd.concat(dfs, ignore_index=True)
        
        # Find total rows exactly like original
        total_row = df[df.apply(lambda row: 'Total' in row.values, axis=1)]
        print("Total rows found:")
        print(total_row)
        
        if total_row.empty:
            raise Exception("No Total rows found in DataFrame")
        
        # Create "Overall Average Ready Time" file exactly like original
        summary_filename = f'Overall Average Ready Time - {target_date_str}.xlsx'
        summary_path = os.path.join(temp_dir, summary_filename)
        
        # Clear sheet first like original clear_sheet() function
        empty_df = pd.DataFrame()
        with pd.ExcelWriter(summary_path, engine='openpyxl') as writer:
            empty_df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        # Save total rows to the file like original
        total_row.to_excel(summary_path, index=False, engine='openpyxl')
        print(f'Created summary file: {summary_filename}')
        
        # STEP 2: Replicate append_new_data() function exactly
        relevant_cols = ['Date', 'Service', 'Successful Op Transfer', 'In Call (Min)', 
                        'Ready (Min)', 'Wrapup (Min)', 'Not Ready (Min)', 'Average Ready Time (Min)']
        
        # Read the file we just created (like original reads from FINAL_FILE_DIRECTORY)
        analysis_df = pd.DataFrame(columns=relevant_cols)
        sheet1_data = pd.read_excel(summary_path, sheet_name='Sheet1')
        print("Processing summary file for analysis...")
        
        # Process columns exactly like original
        for col in relevant_cols:
            if col in sheet1_data.columns:
                if col != 'Service':
                    analysis_df[col] = pd.to_numeric(sheet1_data[col], errors='coerce')
                    print(f'{col} converted to numeric')
                    
                    # Convert (Min) to (Sec) and multiply by 60 like original
                    if '(Min)' in col:
                        new_col_name = col.replace('(Min)', '(Sec)')
                        analysis_df.rename(columns={col: new_col_name}, inplace=True)
                        analysis_df[new_col_name] *= 60
                        print(f'{col} renamed to {new_col_name}')
                else:
                    analysis_df[col] = sheet1_data[col]
                    print(f'{col} processed')
            else:
                print(f'{col} not in sheet1_data.columns')
        
        # Add Date column like original
        analysis_df['Date'] = target_date_str
        
        # Calculate Average Ready Time like original
        analysis_df['Average Ready Time (Sec)'] = analysis_df['Ready (Sec)'] / analysis_df['Successful Op Transfer']
        if 'Average Ready Time (Min)' in analysis_df.columns:
            del analysis_df['Average Ready Time (Min)']
        
        # Handle division by zero like original
        for index, row in analysis_df.iterrows():
            if row['Successful Op Transfer'] != 0:
                analysis_df.at[index, 'Average Ready Time (Sec)'] = row['Average Ready Time (Sec)']
            else:
                analysis_df.at[index, 'Average Ready Time (Sec)'] = 0
        
        # Add TOTAL row exactly like original
        total_index = analysis_df.index.max() + 1
        analysis_df.loc[total_index, 'Service'] = 'TOTAL'
        for col in analysis_df.columns[2:]:
            analysis_df.loc[total_index, col] = analysis_df[col].iloc[:total_index].sum()
        
        # Calculate total average ready time like original
        total_ready_time = analysis_df.loc[total_index, 'Ready (Sec)']
        total_transfers = analysis_df.loc[total_index, 'Successful Op Transfer']
        total_average_ready_time = total_ready_time / total_transfers
        analysis_df.loc[total_index, 'Average Ready Time (Sec)'] = total_average_ready_time
        analysis_df['Average Ready Time (Sec)'] = analysis_df['Average Ready Time (Sec)'].round(2)
        
        # Create bar chart exactly like original
        try:
            colors = ['#009c89'] * len(analysis_df['Service'])
            colors[total_index] = '#7d2300'
            chart_data = analysis_df[['Service', 'Average Ready Time (Sec)']]
            plt.figure(figsize=(10, 6))
            plt.barh(chart_data['Service'], chart_data['Average Ready Time (Sec)'], color=colors)
            for index, value in enumerate(chart_data['Average Ready Time (Sec)']):
                plt.text(value, index, str(value))
            plt.xlabel('Average Ready Time (Sec)')
            plt.ylabel('Service')
            plt.title('Average Ready Time by Service')
            plt.tight_layout()
            chart_path = os.path.join(temp_dir, 'average_ready_time_chart.png')
            plt.savefig(chart_path)
            plt.close()
            print("Created and saved the bar chart")
        except Exception as chart_error:
            print(f"Chart creation failed: {chart_error}")
            chart_path = None
        
        # Add ART sheet to the existing file exactly like original
        try:
            with pd.ExcelWriter(summary_path, engine='openpyxl', mode='a') as writer:
                if 'ART' not in writer.book.sheetnames:
                    analysis_df.to_excel(writer, sheet_name='ART', index=False)
                    print("Appended data to the excel sheet ART")
                
                # Add chart image like original
                if chart_path and os.path.exists(chart_path):
                    idx = writer.book.sheetnames.index('ART')
                    ws = writer.book.worksheets[idx]
                    
                    img = OpenpyxlImage(chart_path)
                    cell = ws.cell(row=16, column=1)
                    ws.add_image(img, cell.coordinate)
                    print("Added chart image to the excel sheet")
                    
                    # Auto-adjust column widths like original
                    for col in ws.columns:
                        max_length = 0
                        column = col[0].column_letter
                        for cell in col:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(cell.value)
                            except:
                                pass
                        adjusted_width = (max_length + 2) * 1.2
                        ws.column_dimensions[column].width = adjusted_width
                    
                    print("Adjusted column widths in the excel sheet")
        
        except Exception as excel_error:
            print(f"Error adding ART sheet: {excel_error}")
        
        print(f'Overall Average Ready Time report created successfully: {summary_filename}')
        update_progress(92, "Report processing completed successfully")
        
    except Exception as e:
        print(f"Error processing HCI files: {e}")
        raise e

# Existing automation functions (keeping all of them)
async def run_automation(task_id: str, config: Dict[str, Any]):
    import time
    start_time = time.time()
    timeout_minutes = 30
    
    try:
        def update_progress(progress: int, message: str):
            if task_id in active_tasks:
                elapsed = int((time.time() - start_time) / 60)
                active_tasks[task_id]['progress'] = progress
                active_tasks[task_id]['message'] = f"{message} (Running {elapsed}m)"
                
                if elapsed >= timeout_minutes:
                    raise Exception(f"Automation timeout after {timeout_minutes} minutes")
        
        # Check for cancellation at key points
        if asyncio.current_task().cancelled():
            raise asyncio.CancelledError("Task was cancelled")
            
        update_progress(5, "Starting browser...")
        
        async with async_playwright() as playwright:
            browser = await playwright.webkit.launch()
            context = await browser.new_context(accept_downloads=True)
            page = await context.new_page()
            await page.set_viewport_size({"width": 1440, "height": 1440})
            page.set_default_timeout(30000)
            
            def handle_page_error(error):
                print(f"Page error: {error}")
            page.on("pageerror", handle_page_error)
            
            try:
                # Check for cancellation
                if asyncio.current_task().cancelled():
                    raise asyncio.CancelledError("Task was cancelled")
                    
                update_progress(10, "Logging in...")
                await page.goto(config['url'])
                await page.locator("#username").fill(config['username'])
                await page.locator("#password").fill(config['password'])
                await page.locator("#password").press("Enter")
                
                update_progress(12, "Waiting for login to complete...")
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(3)
                
                # Check for cancellation
                if asyncio.current_task().cancelled():
                    raise asyncio.CancelledError("Task was cancelled")
                
                update_progress(14, "Verifying login success...")
                try:
                    await page.wait_for_selector("button:has-text('Review')", timeout=15000)
                    update_progress(15, "Login verified - Review button found")
                except Exception as e:
                    update_progress(14, "Review button not immediately found, waiting longer...")
                    await page.wait_for_load_state("domcontentloaded")
                    await asyncio.sleep(2)
                    
                    page_title = await page.title()
                    print(f"Page title: {page_title}")
                    if "login" in page_title.lower() or "sign" in page_title.lower():
                        raise Exception("Login may have failed - still on login page")
                
                # Check for cancellation before automation logic
                if asyncio.current_task().cancelled():
                    raise asyncio.CancelledError("Task was cancelled")
                
                if config['function_type'] == 'specific_calls':
                    await run_specific_calls_logic(page, config, update_progress)
                elif config['function_type'] == 'all_calls':
                    await run_all_calls_logic(page, config, update_progress)
                
                # Check for cancellation before ZIP creation
                if asyncio.current_task().cancelled():
                    raise asyncio.CancelledError("Task was cancelled")
                
                update_progress(95, "Creating ZIP file...")
                zip_file_path = await create_zip_file(task_id, config['temp_dir'], config['agent_id'])
                
                if task_id in active_tasks:
                    active_tasks[task_id]['zip_file'] = zip_file_path
                    active_tasks[task_id]['agent_id'] = config['agent_id']
                
                elapsed = int((time.time() - start_time) / 60)
                update_progress(100, f"Automation completed successfully in {elapsed}m! ZIP file ready for download.")
                active_tasks[task_id]['status'] = 'completed'
                
            except asyncio.CancelledError:
                print(f"LiveVox Task {task_id} was cancelled, cleaning up...")
                raise
            except Exception as e:
                error_msg = str(e)
                if "timeout" in error_msg.lower():
                    update_progress(0, f"Automation timed out: {error_msg}")
                else:
                    update_progress(0, f"Error: {error_msg}")
                active_tasks[task_id]['status'] = 'failed'
            finally:
                # Ensure browser is always closed
                try:
                    await browser.close()
                except:
                    pass
                
    except asyncio.CancelledError:
        # Handle cancellation gracefully
        if task_id in active_tasks:
            active_tasks[task_id]['status'] = 'stopped'
            active_tasks[task_id]['message'] = 'Automation stopped by user'
        print(f"LiveVox Task {task_id} cancelled successfully")
        raise
    except Exception as e:
        if task_id in active_tasks:
            active_tasks[task_id]['status'] = 'failed'
            active_tasks[task_id]['message'] = f"Error: {str(e)}"

async def create_zip_file(task_id: str, temp_dir: str, identifier: str) -> str:
    """Create a ZIP file containing all downloaded files"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f"automation_results_{identifier}_{timestamp}.zip"
    zip_path = os.path.join(tempfile.gettempdir(), zip_filename)
    
    file_count = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
                file_count += 1
    
    print(f"Created ZIP file: {zip_path} with {file_count} files")
    return zip_path

async def run_specific_calls_logic(page, config, update_progress):
    """Implementation for Specific Calls automation logic"""
    agent_details_map = {
        "3P_95": {"folder": "Chuck", "locator_id": "963665"},
        "3P_235": {"folder": "Jim", "locator_id": "976426"},
        "3P_1483": {"folder": "Clifford", "locator_id": "969789"},
        "3P_260": {"folder": "Kathy", "locator_id": "963666"},
        "3P_282": {"folder": "Laurie", "locator_id": "924766"}
    }
    
    current_agent_id = config['agent_id']
    agent_info = agent_details_map.get(current_agent_id)
    
    if not agent_info:
        raise Exception(f"Agent ID '{current_agent_id}' not found in mapping")
    
    calls_to_process = data_manager.get_calls(current_agent_id)
    if not calls_to_process:
        raise Exception(f"No calls configured for agent '{current_agent_id}'")
    
    target_dir = os.path.join(config['temp_dir'], agent_info['folder'])
    os.makedirs(target_dir, exist_ok=True)
    
    update_progress(15, f"Starting automation for {len(calls_to_process)} calls for {agent_info['folder']}")
    
    download_counter = 1
    
    update_progress(18, "Navigating to Call Recording Report...")
    try:
        await page.wait_for_selector("button:has-text('Review')", timeout=30000)
        await page.get_by_role("button", name="Review").click()
        
        await page.wait_for_selector("text=Agent Reports", timeout=15000)
        await page.get_by_text("Agent Reports").click()
        
        update_progress(19, "Waiting for Call Recording Report...")
        await page.wait_for_selector("div.MuiTreeItem-label:has-text('Call Recording Report')", timeout=60000)
        await page.locator("div.MuiTreeItem-label").filter(has_text="Call Recording Report").click()
        
        await page.wait_for_load_state("networkidle")
        update_progress(20, "Report page loaded successfully")
        
    except Exception as nav_error:
        raise Exception(f"Navigation failed: {str(nav_error)}. Make sure you're logged into the correct LiveVox portal.")
    
    update_progress(22, f"Setting up search for agent {current_agent_id}")
    await page.locator("#search-panel__start-date").fill(config['start_date'])
    
    await page.get_by_role("row", name="Agent Select One ... Result").locator("u").click()
    await page.get_by_placeholder("Search...").fill(current_agent_id)
    
    agent_selector = f'[id="\\33 {agent_info["locator_id"]}"]'
    try:
        await page.wait_for_selector(agent_selector, timeout=10000)
        await page.locator(agent_selector).click()
        await page.locator("#agent-combo__ok-btn").click()
        update_progress(24, f"Agent {current_agent_id} selected successfully")
    except Exception as e:
        raise Exception(f"Could not find agent {current_agent_id} (locator: {agent_info['locator_id']}). Check agent mapping.")
    
    for i, call_data in enumerate(calls_to_process):
        progress = 25 + int(((i + 1) / len(calls_to_process)) * 65)
        update_progress(progress, f"Searching call {i+1}/{len(calls_to_process)}: {call_data['phone']} (duration: {call_data['duration']}s)")
        
        await page.locator("#search-panel__phone-dialed").clear()
        await page.locator("#search-panel__phone-dialed").fill(call_data['phone'])
        await page.get_by_role("button", name="Generate Report").click()
        
        try:
            results_table_body = page.locator("div.rt-tbody")
            first_row = results_table_body.locator("div.rt-tr:not(.-padRow)").first
            await first_row.wait_for(state="visible", timeout=15000)
            
            data_rows = await results_table_body.locator("div.rt-tr:not(.-padRow)").all()
            update_progress(progress, f"Found {len(data_rows)} recordings for {call_data['phone']}, checking durations...")
            
            found_match = False
            for j, row in enumerate(data_rows):
                duration_in_row = await row.locator("div.rt-td").nth(8).inner_text()
                if duration_in_row == call_data['duration']:
                    update_progress(progress, f"Found matching duration {duration_in_row}s, downloading...")
                    download_button = row.locator("div.icon--audio-download.clickable")
                    async with page.expect_download() as download_info:
                        await download_button.click()
                    
                    download = await download_info.value
                    base_filename = download.suggested_filename
                    name, ext = os.path.splitext(base_filename)
                    
                    final_filename = f"{name}-{download_counter}{ext}"
                    target_path = os.path.join(target_dir, final_filename)
                    
                    update_progress(progress, f"Saved: {final_filename}")
                    shutil.move(await download.path(), target_path)
                    
                    download_counter += 1
                    found_match = True
                    break
            
            if not found_match:
                update_progress(progress, f"No matching duration found for {call_data['phone']} (needed: {call_data['duration']}s)")
                    
        except Exception as e:
            update_progress(progress, f"No results found for {call_data['phone']}: {str(e)[:50]}")
    
    update_progress(90, f"Completed processing {len(calls_to_process)} calls. Downloaded {download_counter-1} files.")

async def run_all_calls_logic(page, config, update_progress):
    """Implementation for All Calls automation logic"""
    agent_details_map = {
        "3P_95": {"folder": "Chuck", "locator_id": "963665"},
        "3P_235": {"folder": "Jim", "locator_id": "976426"},
        "3P_1483": {"folder": "Clifford", "locator_id": "969789"},
        "3P_260": {"folder": "Kathy", "locator_id": "963666"},
        "3P_282": {"folder": "Laurie", "locator_id": "924766"}
    }
    
    current_agent_id = config['agent_id']
    agent_info = agent_details_map.get(current_agent_id)
    
    if not agent_info:
        raise Exception(f"Agent ID '{current_agent_id}' not found in mapping")
    
    phone_numbers = config['phone_numbers'].split(',')
    phone_numbers = [phone.strip() for phone in phone_numbers if phone.strip()]
    
    if not phone_numbers:
        raise Exception("No valid phone numbers provided")
    
    target_dir = os.path.join(config['temp_dir'], agent_info['folder'])
    os.makedirs(target_dir, exist_ok=True)
    
    update_progress(15, f"Processing {len(phone_numbers)} phone numbers for {agent_info['folder']}")
    
    download_counter = 1
    
    update_progress(18, "Navigating to Call Recording Report...")
    try:
        await page.wait_for_selector("button:has-text('Review')", timeout=30000)
        await page.get_by_role("button", name="Review").click()
        
        await page.wait_for_selector("text=Agent Reports", timeout=15000)
        await page.get_by_text("Agent Reports").click()
        
        update_progress(19, "Waiting for Call Recording Report...")
        await page.wait_for_selector("div.MuiTreeItem-label:has-text('Call Recording Report')", timeout=60000)
        await page.locator("div.MuiTreeItem-label").filter(has_text="Call Recording Report").click()
        
        await page.wait_for_load_state("networkidle")
        update_progress(20, "Report page loaded successfully")
        
    except Exception as nav_error:
        raise Exception(f"Navigation failed: {str(nav_error)}. Make sure you're logged into the correct LiveVox portal.")
    
    update_progress(22, f"Setting up search for agent {current_agent_id}")
    await page.locator("#search-panel__start-date").fill(config['start_date'])
    
    await page.get_by_role("row", name="Agent Select One ... Result").locator("u").click()
    await page.get_by_placeholder("Search...").fill(current_agent_id)
    
    agent_selector = f'[id="\\33 {agent_info["locator_id"]}"]'
    try:
        await page.wait_for_selector(agent_selector, timeout=10000)
        await page.locator(agent_selector).click()
        await page.locator("#agent-combo__ok-btn").click()
        update_progress(24, f"Agent {current_agent_id} selected successfully")
    except Exception as e:
        raise Exception(f"Could not find agent {current_agent_id} (locator: {agent_info['locator_id']}). Check agent mapping.")
    
    for i, phone in enumerate(phone_numbers):
        progress = 25 + int(((i + 1) / len(phone_numbers)) * 65)
        update_progress(progress, f"Processing phone {i+1}/{len(phone_numbers)}: {phone}")
        
        await page.locator("#search-panel__phone-dialed").clear()
        await page.locator("#search-panel__phone-dialed").fill(phone)
        await page.get_by_role("button", name="Generate Report").click()
        
        try:
            results_table_body = page.locator("div.rt-tbody")
            first_row = results_table_body.locator("div.rt-tr:not(.-padRow)").first
            await first_row.wait_for(state="visible", timeout=15000)
            
            data_rows = await results_table_body.locator("div.rt-tr:not(.-padRow)").all()
            
            update_progress(progress, f"Found {len(data_rows)} recording(s) for phone {phone}. Downloading all...")
            
            for row in data_rows:
                download_button = row.locator("div.icon--audio-download.clickable")
                async with page.expect_download() as download_info:
                    await download_button.click()
                
                download = await download_info.value
                base_filename = download.suggested_filename
                name, ext = os.path.splitext(base_filename)
                
                final_filename = f"{name}-{download_counter}{ext}"
                target_path = os.path.join(target_dir, final_filename)
                
                update_progress(progress, f"Saving file: {final_filename}")
                shutil.move(await download.path(), target_path)
                
                download_counter += 1
                
        except Exception as e:
            update_progress(progress, f"No recordings found for phone: {phone}")
    
    update_progress(90, f"Completed processing {len(phone_numbers)} phone numbers. Downloaded {download_counter-1} files.")

if __name__ == "__main__":
    os.makedirs("templates", exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8001)