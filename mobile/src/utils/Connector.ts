class Connector {
    private ports: Map<string, HTMLElement>;

    constructor() {
        this.ports = new Map();
    }

    // Method to add a port with a unique identifier
    public addPort(id: string, element: HTMLElement) {
        this.ports.set(id, element);
    }

    // Method to snap to the nearest port based on a given position
    public snapToPort(position: { x: number; y: number }): { portId: string | null, visualFeedback: boolean } {
        let closestPortId: string | null = null;
        let closestDistance = Infinity;

        // Iterate through all ports to find the closest one
        this.ports.forEach((element, id) => {
            const rect = element.getBoundingClientRect();
            const portCenter = {
                x: rect.left + rect.width / 2,
                y: rect.top + rect.height / 2,
            };

            const distance = this.calculateDistance(position, portCenter);
            if (distance < closestDistance) {
                closestDistance = distance;
                closestPortId = id;
            }
        });

        const snapThreshold = 30; // pixels
        const visualFeedback = closestDistance <= snapThreshold;

        return { portId: visualFeedback ? closestPortId : null, visualFeedback };
    }

    // Private method to calculate the distance between two points
    private calculateDistance(pointA: { x: number; y: number }, pointB: { x: number; y: number }): number {
        return Math.sqrt(Math.pow(pointB.x - pointA.x, 2) + Math.pow(pointB.y - pointA.y, 2));
    }
}

export default Connector;