#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
#include <fstream>
#include <jsoncpp/json/json.h>
#include <chrono>

void readJsonFile(const char* filename) {
    // 读取JSON文件
    std::ifstream file(filename);
    Json::Value jsonData;
    file >> jsonData;

    // 在这里处理jsonData，例如输出到控制台
    std::cout << jsonData << std::endl;
}

int main() {
    const char* filename = "data/inquiry.json";
    const int numProcesses = 1000;
    auto epoch_time = std::chrono::system_clock::now().time_since_epoch();
    long long epoch_seconds = std::chrono::duration_cast<std::chrono::milliseconds>(epoch_time).count();
    for (int i = 0; i < numProcesses; ++i) {
        pid_t pid = fork();

        if (pid == 0) { // 子进程
            readJsonFile(filename);
            exit(0); // 子进程完成后退出
        } else if (pid < 0) {
            std::cerr << "Failed to fork process" << std::endl;
            exit(1);
        }
    }
    
    // 等待所有子进程完成
    while (wait(nullptr) > 0) {}
    
    auto epoch_time1 = std::chrono::system_clock::now().time_since_epoch();
    long long epoch_seconds1 = std::chrono::duration_cast<std::chrono::milliseconds>(epoch_time1).count();
    std::cout << "Time elapsed: " << epoch_seconds1 - epoch_seconds << " seconds" << std::endl;
    return 0;
}
