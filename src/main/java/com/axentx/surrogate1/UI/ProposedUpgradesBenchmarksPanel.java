import javax.swing.*;
import java.awt.*;

public class ProposedUpgradesBenchmarksPanel extends JPanel {
    public ProposedUpgradesBenchmarksPanel(List<Benchmark> benchmarks) {
        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        for (Benchmark benchmark : benchmarks) {
            add(new BenchmarkPanel(benchmark));
        }
    }
}