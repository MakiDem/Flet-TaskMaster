import uuid
from datetime import datetime, timedelta
from database.init_db import get_connection


def _row_to_dict(row):
    """Convert sqlite Row to dictionary."""
    if row is None:
        return None
    return dict(row)


def _rows_to_list(rows):
    """Convert list of sqlite Rows to list of dictionaries."""
    return [dict(row) for row in rows]


# ============================================================
# CREATE
# ============================================================

def create_task(task):
    """
    Create a new task.
    
    Returns:
        dict: The created task
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    task_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    cursor.execute('''
        INSERT INTO tasks (id, title, description, status, priority, due_date, category, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (task_id, task.get("title"), task.get("description", ""), task.get("status", "pending"), task.get("priority", "medium"), task.get("due_date"), task.get("category", "work"), now, now))
    
    conn.commit()
    conn.close()
    
    return {
        "id": task_id,
        "title": task.get("title"),
        "description": task.get("description", ""),
        "status": task.get("status", "pending"),
        "priority": task.get("priority", "medium"),
        "due_date": task.get("due_date") if task.get("due_date") else (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "category": task.get("category", "work"),
        "created_at": now,
        "updated_at": now
    }


# ============================================================
# READ
# ============================================================

def get_all_tasks():
    """
    Get all tasks.
    
    Returns:
        list: List of all tasks as dictionaries
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
    rows = cursor.fetchall()
    
    conn.close()
    update_overdue_tasks()
    return _rows_to_list(rows)


def get_task_by_id(task_id):
    """
    Get a single task by ID.
    
    Returns:
        dict or None: Task dictionary or None if not found
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    
    conn.close()
    return _row_to_dict(row)


def get_tasks_by_status(status):
    """
    Get tasks filtered by status.
    
    Args:
        status: 'pending', 'completed', or 'overdue'
    
    Returns:
        list: Filtered tasks
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC', (status,))
    rows = cursor.fetchall()
    
    conn.close()
    return _rows_to_list(rows)


# ============================================================
# UPDATE
# ============================================================

def update_task(task_id, **kwargs):
    """
    Update a task.
    
    Args:
        task_id: ID of task to update
        **kwargs: Fields to update (title, description, status, priority, due_date)
    
    Returns:
        dict or None: Updated task or None if not found
    """
    allowed_fields = [
        'title', 'description', 'status', 'priority',
        'due_date', 'category', 'date'
    ]
    updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not updates:
        return get_task_by_id(task_id)
    
    updates['updated_at'] = datetime.now().isoformat()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    set_clause = ', '.join([f'{key} = ?' for key in updates.keys()])
    values = list(updates.values()) + [task_id]
    
    cursor.execute(f'UPDATE tasks SET {set_clause} WHERE id = ?', values)
    
    conn.commit()
    conn.close()
    
    return get_task_by_id(task_id)


# ============================================================
# DELETE
# ============================================================

def delete_task(task_id):
    """
    Delete a task.
    
    Args:
        task_id: ID of task to delete
    
    Returns:
        bool: True if deleted, False if not found
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    deleted = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    return deleted


# ============================================================
# AUTO-OVERDUE FUNCTIONALITY
# ============================================================

def update_overdue_tasks():
    """
    Automatically update pending tasks to overdue if due_date has passed.
    
    This function:
    - Finds all tasks with status='pending'
    - Checks if their due_date is before today
    - Updates their status to 'overdue'
    
    Returns:
        int: Number of tasks updated to overdue
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    today = datetime.now().date().isoformat()
    
    # Update all pending tasks where due_date is before today
    cursor.execute('''
        UPDATE tasks 
        SET status = 'overdue', updated_at = ?
        WHERE status = 'pending' 
        AND due_date < ?
        AND due_date IS NOT NULL
    ''', (datetime.now().isoformat(), today))
    
    updated_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return updated_count


def get_all_tasks_with_auto_overdue():
    """
    Get all tasks and automatically update overdue status.
    
    This is a convenience function that:
    1. Updates overdue tasks
    2. Returns all tasks
    
    Returns:
        list: List of all tasks as dictionaries
    """
    update_overdue_tasks()
    return get_all_tasks()


def get_tasks_by_status_with_auto_overdue(status):
    """
    Get tasks by status and automatically update overdue status.
    
    Args:
        status: 'pending', 'completed', or 'overdue'
    
    Returns:
        list: Filtered tasks
    """
    update_overdue_tasks()
    return get_tasks_by_status(status)


# ============================================================
# UTILITY
# ============================================================

def get_task_counts():
    """
    Get counts of tasks by status.
    
    Returns:
        dict: {'total': int, 'pending': int, 'completed': int, 'overdue': int}
    """
    # Update overdue tasks before counting
    update_overdue_tasks()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM tasks WHERE due_date = date("now")')
    total = cursor.fetchone()['count']

    today_completed = 0
    cursor.execute('SELECT COUNT(*) as count FROM tasks WHERE due_date = date("now") AND status = "completed"')
    today_completed = cursor.fetchone()['count']
    
    cursor.execute('SELECT status, COUNT(*) as count FROM tasks GROUP BY status')
    rows = cursor.fetchall()
    
    conn.close()
    
    counts = {'today_completed': today_completed, 'today_total': total, 'pending': 0, 'completed': 0, 'overdue': 0}
    for row in rows:
        counts[row['status']] = row['count']
    
    return counts

def get_today_tasks():
    """
    Get tasks that are due today.
    
    Returns:
        list: Tasks due today
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks WHERE due_date = date("now", "localtime") ORDER BY created_at DESC')
    rows = cursor.fetchall()
    
    conn.close()
    return _rows_to_list(rows)


# ============================================================
# SEARCH
# ============================================================
def search_tasks(query, limit=5):
    """
    Search tasks by title or description using a case-insensitive LIKE query.

    Args:
        query: search string
        limit: maximum number of results

    Returns:
        list of task dicts
    """
    if not query:
        return []

    q = f"%{query.strip().lower()}%"
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''SELECT * FROM tasks WHERE LOWER(title) LIKE ? OR LOWER(description) LIKE ? ORDER BY created_at DESC LIMIT ?''',
        (q, q, limit)
    )
    rows = cursor.fetchall()
    conn.close()

    return _rows_to_list(rows)