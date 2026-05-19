import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class WorkflowUI extends JFrame {
    private JButton createWorkflowButton;
    private JButton manageWorkflowButton;
    private JPanel mainPanel;

    public WorkflowUI() {
        createWorkflowButton = new JButton("Create Workflow");
        manageWorkflowButton = new JButton("Manage Workflow");
        mainPanel = new JPanel();

        createWorkflowButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Create workflow logic here
                System.out.println("Create workflow button clicked");
            }
        });

        manageWorkflowButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Manage workflow logic here
                System.out.println("Manage workflow button clicked");
            }
        });

        mainPanel.add(createWorkflowButton);
        mainPanel.add(manageWorkflowButton);

        this.add(mainPanel);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.pack();
        this.setVisible(true);
    }

    public static void main(String[] args) {
        new WorkflowUI();
    }
}