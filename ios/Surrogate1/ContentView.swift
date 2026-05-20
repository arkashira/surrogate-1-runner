import SwiftUI

struct ContentView: View {
    var body: some View {
        NavigationView {
            VStack {
                Text("Surrogate-1 Workflow Automation")
                    .font(.largeTitle)
                    .padding()

                NavigationLink(destination: WorkflowsView()) {
                    Text("Start Automating")
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
            }
            .navigationTitle("Home")
        }
    }
}