// Global Progress State Management System
window.GlobalProgressManager = {
    STORAGE_KEY: 'livevox_active_tasks',
    TTL_HOURS: 24, // Task expiration time in hours
    SYNC_INTERVAL: 30000, // Server sync interval (30 seconds)
    CLEANUP_INTERVAL: 5 * 60 * 1000, // Cleanup interval (5 minutes)
    
    // Task type mappings for display
    TASK_TYPES: {
        'call': 'Call Automation',
        'hci': 'HCI Summary',
        'phrases': 'Add Phrases'
    },
    
    // Page mappings for navigation
    PAGE_URLS: {
        'call': '/livevox',
        'hci': '/hci-summary', 
        'phrases': '/add-phrases'
    },

    // Get all active tasks from localStorage
    getTasks: function() {
        try {
            const tasks = localStorage.getItem(this.STORAGE_KEY);
            return tasks ? JSON.parse(tasks) : [];
        } catch (error) {
            console.error('Error reading global progress tasks:', error);
            return [];
        }
    },

    // Save tasks to localStorage
    saveTasks: function(tasks) {
        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(tasks));
            this.syncUI();
        } catch (error) {
            console.error('Error saving global progress tasks:', error);
        }
    },

    // Add or update a task
    updateTask: function(taskData) {
        let tasks = this.getTasks();
        const existingIndex = tasks.findIndex(task => task.task_id === taskData.task_id);
        
        const now = new Date();
        const updatedTask = {
            task_id: taskData.task_id,
            type: taskData.type,
            progress: taskData.progress || 0,
            message: taskData.message || 'Starting...',
            start_time: taskData.start_time || now.toISOString(),
            source_page: taskData.source_page || window.location.pathname,
            status: taskData.status || 'running',
            last_updated: now.toISOString(),
            expires_at: new Date(now.getTime() + (this.TTL_HOURS * 60 * 60 * 1000)).toISOString(),
            resumed: taskData.resumed || false // Flag to indicate if task was resumed from storage
        };

        if (existingIndex >= 0) {
            // Preserve original start time and update other fields
            updatedTask.start_time = tasks[existingIndex].start_time;
            updatedTask.expires_at = tasks[existingIndex].expires_at;
            tasks[existingIndex] = updatedTask;
        } else {
            tasks.push(updatedTask);
        }

        this.saveTasks(tasks);
    },

    // Remove a task
    removeTask: function(task_id) {
        let tasks = this.getTasks();
        tasks = tasks.filter(task => task.task_id !== task_id);
        this.saveTasks(tasks);
    },

    // Get a specific task
    getTask: function(task_id) {
        const tasks = this.getTasks();
        return tasks.find(task => task.task_id === task_id);
    },

    // Clean up old/completed tasks with improved TTL handling
    cleanupTasks: function() {
        let tasks = this.getTasks();
        const now = new Date();
        let cleanedCount = 0;
        
        tasks = tasks.filter(task => {
            // Check if task has expired based on expires_at field
            if (task.expires_at && new Date(task.expires_at) <= now) {
                cleanedCount++;
                return false;
            }
            
            // Fallback to old method if expires_at is not set
            const taskAge = now - new Date(task.start_time);
            const maxAge = this.TTL_HOURS * 60 * 60 * 1000;
            if (taskAge > maxAge) {
                cleanedCount++;
                return false;
            }
            
            // Remove completed or error tasks older than 1 hour
            if ((task.status === 'completed' || task.status === 'error') && taskAge > 60 * 60 * 1000) {
                cleanedCount++;
                return false;
            }
            
            return true;
        });
        
        if (cleanedCount > 0) {
            console.log(`GlobalProgressManager: Cleaned up ${cleanedCount} expired tasks`);
            this.saveTasks(tasks);
        }
    },

    // Update the UI to show current tasks
    syncUI: function() {
        const tasks = this.getTasks();
        const globalProgress = document.getElementById('globalProgress');
        const tasksContainer = document.getElementById('globalProgressTasks');
        
        if (!globalProgress || !tasksContainer) return;

        if (tasks.length === 0) {
            globalProgress.style.display = 'none';
            return;
        }

        globalProgress.style.display = 'block';
        tasksContainer.innerHTML = '';

        tasks.forEach(task => {
            const taskElement = this.createTaskElement(task);
            tasksContainer.appendChild(taskElement);
        });
    },

    // Create a task UI element
    createTaskElement: function(task) {
        const taskDiv = document.createElement('div');
        taskDiv.className = 'progress-task';
        taskDiv.setAttribute('data-task-id', task.task_id);

        const elapsedTime = this.getElapsedTime(task.start_time);
        const taskTypeName = this.TASK_TYPES[task.type] || task.type;
        const progressPercent = Math.max(0, Math.min(100, task.progress || 0));
        
        // Visual indicator for resumed tasks
        const resumedIndicator = task.resumed ? ' <span style="color: #666; font-size: 11px;">(Resumed)</span>' : '';
        
        // Status-based styling
        const statusClass = task.status === 'completed' ? 'completed' : 
                           task.status === 'error' ? 'error' : 'running';

        taskDiv.innerHTML = `
            <div class="progress-task-header">
                <span class="progress-task-type">${taskTypeName}${resumedIndicator}</span>
                <div class="progress-task-controls">
                    <button class="progress-task-btn" onclick="GlobalProgressManager.goToTask('${task.task_id}')">View</button>
                    ${task.status === 'running' ? 
                        `<button class="progress-task-btn" onclick="GlobalProgressManager.stopTask('${task.task_id}')">Stop</button>` : 
                        `<button class="progress-task-btn" onclick="GlobalProgressManager.removeTask('${task.task_id}')">Remove</button>`
                    }
                </div>
            </div>
            <div class="progress-task-bar">
                <div class="progress-task-fill progress-${statusClass}" style="width: ${progressPercent}%"></div>
            </div>
            <div class="progress-task-message">${task.message}</div>
            <div class="progress-task-time">
                ${task.status === 'running' ? `Running for ${elapsedTime}` : 
                  task.status === 'completed' ? `Completed ${this.getRelativeTime(task.last_updated)}` :
                  task.status === 'error' ? `Failed ${this.getRelativeTime(task.last_updated)}` : 
                  `Running for ${elapsedTime}`}
            </div>
        `;

        return taskDiv;
    },

    // Calculate elapsed time string
    getElapsedTime: function(startTime) {
        const start = new Date(startTime);
        const now = new Date();
        const diffMs = now - start;
        const diffMins = Math.floor(diffMs / 60000);
        
        if (diffMins < 1) return 'less than 1 minute';
        if (diffMins < 60) return `${diffMins} minute${diffMins !== 1 ? 's' : ''}`;
        
        const hours = Math.floor(diffMins / 60);
        const mins = diffMins % 60;
        return `${hours}h ${mins}m`;
    },

    // Get relative time string (e.g., "5 minutes ago")
    getRelativeTime: function(timestamp) {
        if (!timestamp) return '';
        
        const time = new Date(timestamp);
        const now = new Date();
        const diffMs = now - time;
        const diffMins = Math.floor(diffMs / 60000);
        
        if (diffMins < 1) return 'just now';
        if (diffMins < 60) return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
        
        const hours = Math.floor(diffMins / 60);
        if (hours < 24) return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
        
        const days = Math.floor(hours / 24);
        return `${days} day${days !== 1 ? 's' : ''} ago`;
    },

    // Sync with server to get current task states
    syncWithServer: function() {
        const tasks = this.getTasks();
        if (tasks.length === 0) return;

        const taskIds = tasks.map(task => task.task_id);
        
        fetch('/api/tasks/status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ task_ids: taskIds })
        })
        .then(response => response.json())
        .then(serverTasks => {
            let updated = false;
            
            tasks.forEach(localTask => {
                const serverTask = serverTasks.find(st => st.task_id === localTask.task_id);
                if (serverTask) {
                    // Update local task with server data
                    if (localTask.progress !== serverTask.progress || 
                        localTask.status !== serverTask.status ||
                        localTask.message !== serverTask.message) {
                        
                        localTask.progress = serverTask.progress;
                        localTask.status = serverTask.status;
                        localTask.message = serverTask.message;
                        localTask.last_updated = new Date().toISOString();
                        updated = true;
                    }
                } else if (localTask.status === 'running') {
                    // Server doesn't know about this task, it might have been stopped/completed
                    localTask.status = 'error';
                    localTask.message = 'Task not found on server (may have been stopped)';
                    localTask.last_updated = new Date().toISOString();
                    updated = true;
                }
            });
            
            if (updated) {
                this.saveTasks(tasks);
            }
        })
        .catch(error => {
            console.log('GlobalProgressManager: Server sync failed (this is normal if no tasks are running):', error);
        });
    },

    // Navigate to the page where the task is running
    goToTask: function(task_id) {
        const task = this.getTask(task_id);
        if (task && this.PAGE_URLS[task.type]) {
            window.location.href = this.PAGE_URLS[task.type];
        }
    },

    // Stop a running task
    stopTask: function(task_id) {
        if (confirm('Are you sure you want to stop this task?')) {
            fetch(`/api/automation/${task_id}/stop`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.removeTask(task_id);
                    }
                })
                .catch(error => {
                    console.error('Error stopping task:', error);
                });
        }
    },

    // Initialize the global progress system
    init: function() {
        console.log('GlobalProgressManager: Initializing...');
        
        // Clean up old tasks on load
        this.cleanupTasks();
        
        // Initial server sync to restore tasks
        setTimeout(() => this.syncWithServer(), 1000);
        
        // Initial UI sync
        this.syncUI();
        
        // Listen for storage changes from other tabs
        window.addEventListener('storage', (e) => {
            if (e.key === this.STORAGE_KEY) {
                console.log('GlobalProgressManager: Storage changed, syncing UI');
                this.syncUI();
            }
        });

        // Listen for page visibility changes to sync when user returns
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                console.log('GlobalProgressManager: Page became visible, syncing...');
                this.syncWithServer();
                this.syncUI();
            }
        });

        // Periodic cleanup and refresh with improved intervals
        setInterval(() => {
            this.cleanupTasks();
        }, this.CLEANUP_INTERVAL);

        // Periodic server sync to keep tasks updated
        setInterval(() => {
            if (!document.hidden) { // Only sync when page is visible
                this.syncWithServer();
            }
        }, this.SYNC_INTERVAL);

        // Update UI every 10 seconds to refresh time displays
        setInterval(() => {
            if (this.getTasks().length > 0) {
                this.syncUI();
            }
        }, 10000);

        console.log('GlobalProgressManager: Initialized successfully');
    }
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => window.GlobalProgressManager.init());
} else {
    window.GlobalProgressManager.init();
}