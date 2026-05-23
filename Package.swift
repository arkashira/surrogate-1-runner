// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "paste_cascade",
    platforms: [.macOS(.v13)],          // requires macOS for AppleScript
    products: [
        .library(name: "PasteCascade", targets: ["PasteCascade"]),
    ],
    targets: [
        .target(name: "PasteCascade"),
        .testTarget(name: "PasteCascadeTests", dependencies: ["PasteCascade"]),
    ]
)