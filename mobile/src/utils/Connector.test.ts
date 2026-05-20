import Connector from './Connector';

describe('Connector', () => {
    let connector: Connector;
    let mockElement: HTMLElement;

    beforeEach(() => {
        connector = new Connector();
        mockElement = document.createElement('div');
        mockElement.style.width = '10px';
        mockElement.style.height = '10px';
        document.body.appendChild(mockElement);
    });

    afterEach(() => {
        document.body.removeChild(mockElement);
    });

    test('should add a port and snap to it', () => {
        connector.addPort('port1', mockElement);
        const position = { x: 5, y: 5 }; // Center of the mockElement
        const { portId, visualFeedback } = connector.snapToPort(position);
        expect(portId).toBe('port1');
        expect(visualFeedback).toBe(true);
    });

    test('should return null if no ports are available', () => {
        const position = { x: 50, y: 50 };
        const { portId, visualFeedback } = connector.snapToPort(position);
        expect(portId).toBeNull();
        expect(visualFeedback).toBe(false);
    });

    test('should not snap if distance is greater than threshold', () => {
        connector.addPort('port1', mockElement);
        const position = { x: 100, y: 100 }; // Far from the mockElement
        const { portId, visualFeedback } = connector.snapToPort(position);
        expect(portId).toBeNull();
        expect(visualFeedback).toBe(false);
    });
});