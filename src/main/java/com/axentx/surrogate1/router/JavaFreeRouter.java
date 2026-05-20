import org.kicad.kicadxml.KicadXml;
import org.kicad.kicadxml.KicadXmlFactory;

public class JavaFreeRouter {
    public static void route(Circuit circuit) {
        // Convert the KiCAD circuit to a KicadXml object
        KicadXml kicadXml = KicadXmlFactory.parse(circuit);

        // Perform the routing using the new algorithm
        kicadXml = new RoutingAlgorithm().route(kicadXml);

        // Convert the updated KicadXml object back to a KiCAD circuit
        circuit = KicadXmlFactory.create(circuit, kicadXml);
    }
}