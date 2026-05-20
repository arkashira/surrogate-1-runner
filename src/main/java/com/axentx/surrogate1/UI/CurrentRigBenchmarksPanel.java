import javax.swing.*;
import java.awt.*;

public class CurrentRigBenchmarksPanel extends JPanel {
    public CurrentRigBenchmarksPanel(List<Benchmark> benchmarks) {
        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        for (Benchmark benchmark : benchmarks) {
            add(new BenchmarkPanel(benchmark));
        }
    }
}