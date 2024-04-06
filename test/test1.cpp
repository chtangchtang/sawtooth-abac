#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
#include <fstream>
#include <jsoncpp/json/json.h>

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

    return 0;
}
