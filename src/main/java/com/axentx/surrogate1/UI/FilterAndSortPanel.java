import javax.swing.*;
import java.awt.*;

public class FilterAndSortPanel extends JPanel {
    public FilterAndSortPanel(List<Benchmark> currentRigBenchmarks, List<Benchmark> proposedUpgradesBenchmarks) {
        setLayout(new FlowLayout());
        add(new JButton("Filter"));
        add(new JButton("Sort"));
    }
}