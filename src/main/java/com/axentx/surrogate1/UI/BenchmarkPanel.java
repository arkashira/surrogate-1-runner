import javax.swing.*;
import java.awt.*;

public class BenchmarkPanel extends JPanel {
    private Benchmark benchmark;

    public BenchmarkPanel(Benchmark benchmark) {
        this.benchmark = benchmark;
        setLayout(new FlowLayout());
        add(new JLabel("Component: " + benchmark.getComponent()));
        add(new JLabel("Benchmark: " + benchmark.getBenchmark()));
    }
}