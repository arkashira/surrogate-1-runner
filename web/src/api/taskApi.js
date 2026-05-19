import axios from 'axios';

const updateTaskStatus = async (taskId, newStatus) => {
  try {
    const response = await axios.patch(`/api/tasks/${taskId}`, { status: newStatus });
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

export default updateTaskStatus;