class Task {
  constructor(id, title, description, status) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.status = status;
  }

  updateStatus(newStatus) {
    this.status = newStatus;
  }
}

export default Task;