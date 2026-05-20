#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#include <cstdlib> // for system()

class CppFormatter {
public:
    /**
     * Formats C++ code using clang-format with a specified style.
     * @param code The source code to format.
     * @param style The formatting style (e.g., "Google", "LLVM", "Mozilla").
     * @return The formatted code as a string.
     * @throws std::runtime_error if clang-format fails.
     */
    std::string format(const std::string& code, const std::string& style = "Google") {
        // Create a temporary file to avoid modifying the original input.
        std::string tempFile = "/tmp/cpp_format_temp.cpp";
        std::ofstream temp(tempFile);
        if (!temp) {
            throw std::runtime_error("Failed to create temporary file");
        }
        temp << code;
        temp.close();

        // Execute clang-format with the specified style.
        std::string command = "clang-format -i -style=" + style + " " + tempFile;
        int result = system(command.c_str());

        if (result != 0) {
            std::remove(tempFile.c_str()); // Clean up on error
            throw std::runtime_error("Clang-format failed to format code");
        }

        // Read the formatted content back.
        std::ifstream formatted(tempFile);
        std::stringstream buffer;
        buffer << formatted.rdbuf();
        std::string formattedCode = buffer.str();

        // Clean up the temporary file.
        std::remove(tempFile.c_str());

        return formattedCode;
    }
};