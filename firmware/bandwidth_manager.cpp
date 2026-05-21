#include <iostream>
#include <vector>
#include <algorithm>

// Structure to represent a GPU
struct GPU {
    int id;
    int bandwidth;
};

// Function to calculate the optimal bandwidth allocation
std::vector<int> calculateBandwidthAllocation(const std::vector<GPU>& gpus) {
    int totalBandwidth = 0;
    for (const auto& gpu : gpus) {
        totalBandwidth += gpu.bandwidth;
    }

    std::vector<int> allocation(gpus.size());
    for (int i = 0; i < gpus.size(); ++i) {
        allocation[i] = static_cast<int>((static_cast<float>(gpus[i].bandwidth) / totalBandwidth) * 100);
    }

    return allocation;
}

// Function to detect and configure multiple GPUs
void detectAndConfigureGPUs() {
    // Simulate detecting 2-4 compatible GPUs
    std::vector<GPU> gpus = {{1, 100}, {2, 150}, {3, 200}, {4, 250}};

    // Calculate the optimal bandwidth allocation
    std::vector<int> allocation = calculateBandwidthAllocation(gpus);

    // Display the allocation
    for (int i = 0; i < gpus.size(); ++i) {
        std::cout << "GPU " << gpus[i].id << ": " << allocation[i] << "%" << std::endl;
    }
}

int main() {
    detectAndConfigureGPUs();
    return 0;
}