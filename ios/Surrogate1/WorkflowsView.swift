import SwiftUI

struct WorkflowsView: View {
    var body: some View {
        List {
            Text("Workflow 1")
            Text("Workflow 2")
            Text("Workflow 3")
        }
        .navigationTitle("Workflows")
    }
}