#include <iostream>
#include <sstream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <chrono>
#include <ctime>
#include <vector>

int main() {
    auto epoch_time = std::chrono::system_clock::now().time_since_epoch();
    long long epoch_seconds = std::chrono::duration_cast<std::chrono::seconds>(epoch_time).count();
    
    int parallelProcesses = 1000; // 设置并行进程数
    const char* command = "abac check data/inquiry.json --url http://192.168.176.27:8086"; // 要执行的Linux终端命令

    for (int i = 0; i < parallelProcesses; ++i) {
        pid_t pid = fork();

        if (pid == 0) {
            // 子进程执行命令
            std::system(command);
            exit(0); // 子进程执行完毕后退出
        }
    }

    // 等待所有子进程执行完毕
    for (int i = 0; i < parallelProcesses; ++i) {
        waitpid(-1, NULL, 0);
    }

    // 输出测试开始的时间戳
    std::cout << "epoch_seconds: " << std::to_string(epoch_seconds) << std::endl;
    
    return 0;
}
