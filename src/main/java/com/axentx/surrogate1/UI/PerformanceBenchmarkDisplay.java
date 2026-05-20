import javax.swing.*;
import java.awt.*;
import java.util.*;

public class PerformanceBenchmarkDisplay extends JPanel {
    private List<Benchmark> currentRigBenchmarks;
    private List<Benchmark> proposedUpgradesBenchmarks;

    public PerformanceBenchmarkDisplay() {
        setLayout(new BorderLayout());
        currentRigBenchmarks = new ArrayList<>();
        proposedUpgradesBenchmarks = new ArrayList<>();
        add(new CurrentRigBenchmarksPanel(currentRigBenchmarks), BorderLayout.NORTH);
        add(new ProposedUpgradesBenchmarksPanel(proposedUpgradesBenchmarks), BorderLayout.CENTER);
        add(new FilterAndSortPanel(currentRigBenchmarks, proposedUpgradesBenchmarks), BorderLayout.SOUTH);
    }

    public void updateCurrentRigBenchmarks(List<Benchmark> benchmarks) {
        currentRigBenchmarks = benchmarks;
        repaint();
    }

    public void updateProposedUpgradesBenchmarks(List<Benchmark> benchmarks) {
        proposedUpgradesBenchmarks = benchmarks;
        repaint();
    }

    private class CurrentRigBenchmarksPanel extends JPanel {
        public CurrentRigBenchmarksPanel(List<Benchmark> benchmarks) {
            setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
            for (Benchmark benchmark : benchmarks) {
                add(new BenchmarkPanel(benchmark));
            }
        }
    }

    private class ProposedUpgradesBenchmarksPanel extends JPanel {
        public ProposedUpgradesBenchmarksPanel(List<Benchmark> benchmarks) {
            setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
            for (Benchmark benchmark : benchmarks) {
                add(new BenchmarkPanel(benchmark));
            }
        }
    }

    private class FilterAndSortPanel extends JPanel {
        public FilterAndSortPanel(List<Benchmark> currentRigBenchmarks, List<Benchmark> proposedUpgradesBenchmarks) {
            setLayout(new FlowLayout());
            add(new JButton("Filter"));
            add(new JButton("Sort"));
        }
    }

    private class BenchmarkPanel extends JPanel {
        private Benchmark benchmark;

        public BenchmarkPanel(Benchmark benchmark) {
            this.benchmark = benchmark;
            setLayout(new FlowLayout());
            add(new JLabel("Component: " + benchmark.getComponent()));
            add(new JLabel("Benchmark: " + benchmark.getBenchmark()));
        }
    }
}

class Benchmark {
    private String component;
    private String benchmark;

    public Benchmark(String component, String benchmark) {
        this.component = component;
        this.benchmark = benchmark;
    }

    public String getComponent() {
        return component;
    }

    public String getBenchmark() {
        return benchmark;
    }
}