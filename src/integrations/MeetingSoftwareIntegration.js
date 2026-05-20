class MeetingSoftwareIntegration {
  constructor() {
    this.integratedSoftware = [];
  }

  integrateWithMeetingSoftware(meetingSoftware) {
    if (!this.integratedSoftware.includes(meetingSoftware)) {
      this.integratedSoftware.push(meetingSoftware);
      return true;
    }
    return false;
  }

  removeIntegration(meetingSoftware) {
    const index = this.integratedSoftware.indexOf(meetingSoftware);
    if (index !== -1) {
      this.integratedSoftware.splice(index, 1);
      return true;
    }
    return false;
  }

  getIntegratedSoftware() {
    return this.integratedSoftware;
  }
}

export default MeetingSoftwareIntegration;