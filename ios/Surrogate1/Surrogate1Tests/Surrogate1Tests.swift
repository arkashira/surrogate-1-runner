import XCTest
@testable import Surrogate1

class Surrogate1Tests: XCTestCase {

    func testExample() {
        XCTAssertTrue(true)
    }

    func testContentView() {
        let view = ContentView()
        let _ = view.body
    }

    func testWorkflowsView() {
        let view = WorkflowsView()
        let _ = view.body
    }
}